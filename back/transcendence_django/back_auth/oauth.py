import base64
import hashlib
import logging
import random
import string
from typing import Dict, Tuple

import requests
from django.conf import settings
from django.contrib.auth import login
from django.core.cache import cache
from shared_models.models import CustomUser

logger = logging.getLogger(__name__)


class OAuthBackend:
    STATE_TIMEOUT = 600

    def __init__(self):
        self.state = ""

    def get_authorize_url(self) -> str:
        self._generate_state()
        url = (
            f"https://api.intra.42.fr/oauth/authorize?client_id={settings.OAUTH_CLIENT_UID}"
            f"&redirect_uri={settings.OAUTH_REDIRECT_URI}"
            f"&response_type=code&scope=public&state={self.state}"
        )

        logger.info("Authorization URL: %s", url)
        return url

    def register_user(self, request, code: str, state: str):
        token_response = self._request_token(code, state)

        if token_response.status_code == 200:
            self._clear_cache(state)
            token_data = token_response.json()
            user, created = self._process_token_data(token_data)
            if not created:
                login(request, user)
            token_response.user_id = user.id
            token_response.new_user_created = created

        return token_response

    def _clear_cache(self, state: str):
        cache.delete(state)

    def _process_token_data(
        self, token_data: Dict[str, str]
    ) -> Tuple[CustomUser, bool]:
        username = self._fetch_username(token_data["access_token"])
        user, created = CustomUser.objects.get_or_create(login42=username)

        if created:
            user.store_tokens(token_data)
        elif not user.username:
            created = True
            logger.info("User created but username is not set")
        else:
            logger.info("User already exists with username: %s", user.username)

        return user, created

    def _request_token(self, code: str, state: str):
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.OAUTH_CLIENT_UID,
            "client_secret": settings.OAUTH_CLIENT_SECRET,
            "code": code,
            "redirect_uri": settings.OAUTH_REDIRECT_URI,
            "state": cache.get(state),
        }
        return requests.post(settings.OAUTH_TOKEN_URL, data=data, timeout=5)

    def _generate_state(self):
        code_verifier = self._generate_code_verifier()
        self.state = self._encode_state(code_verifier)
        cache.set(self.state, code_verifier, timeout=self.STATE_TIMEOUT)

    def _generate_code_verifier(self) -> str:
        return "".join(
            random.choices(
                string.ascii_uppercase + string.digits, k=random.randint(43, 128)
            )
        )

    def _encode_state(self, code_verifier: str) -> str:
        state_bytes = hashlib.sha256(code_verifier.encode("utf-8")).digest()
        state_encoded = (
            base64.urlsafe_b64encode(state_bytes).decode("utf-8").rstrip("=")
        )
        return state_encoded

    def _fetch_username(self, access_token: str) -> str:
        user_info_url = "https://api.intra.42.fr/v2/me"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(user_info_url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.json().get("login", "")
