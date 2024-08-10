import logging
import random
import string
import base64
import hashlib
import requests
from django.core.cache import cache
from django.conf import settings
from shared_models.models import CustomUser
from django.contrib.auth import login

logger = logging.getLogger(__name__)


class OAuthBackend(object):

	def __init__(self):
		self.state: str = ""

	def get_authorize_url(self) -> str:
		self.__generate_code()
		url: str = f"https://api.intra.42.fr/oauth/authorize?client_id={settings.OAUTH_CLIENT_UID}&redirect_uri={settings.OAUTH_REDIRECT_URI}&response_type=code&scope=public&state={self.state}'"
		logger.info("url: %s", url)
		return url

	def signin(self, request, code: str, state: str) -> int:
		response_token = self.__request_for_token(state, code)

		if response_token.status_code == 200:
			self.clear_cache(state)
			token_data = response_token.json()
			user = self.process_token_data(token_data)
			login(request, user)
		return response_token.status_code

	def clear_cache(self, state: str):
		cache.delete(state)

	def process_token_data(self, token_data: dict):
		login42 = self.__get_username(token_data["access_token"])
		user, created = CustomUser.objects.get_or_create(username=login42, login42=login42)

		if created:
			user.store_tokens(token_data)
		return user

	def __request_for_token(self, state: str, code: str):
		data = {
			"grant_type": "authorization_code",
			"client_id": settings.OAUTH_CLIENT_UID,
			"client_secret": settings.OAUTH_CLIENT_SECRET,
			"code": code,
			"redirect_uri": settings.OAUTH_REDIRECT_URI,
			"state":  cache.get(state),
		}
		return requests.post(settings.OAUTH_TOKEN_URL, data=data)

	def __generate_code(self):
		code_verifier = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
		self.state = hashlib.sha256(code_verifier.encode('utf-8')).digest()
		self.state = base64.urlsafe_b64encode(self.state).decode('utf-8').replace('=', '')
		cache.set(self.state, code_verifier, timeout=600)

	def __get_username(self, access_token):
		user_info_url = "https://api.intra.42.fr/v2/me"
		headers = {
			"Authorization": f"Bearer {access_token}",
		}
		response = requests.get(user_info_url, headers=headers)
		response.raise_for_status()
		return response.json()["login"]



