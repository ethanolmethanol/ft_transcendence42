import logging
import random
import string
import base64
import hashlib
import requests
from django.core.cache import cache
from django.conf import settings

logger = logging.getLogger(__name__)


class OAuthBackend(object):

	def __init__(self):
		self.state: str = ""

	def get_authorize_url(self) -> str:
		self.__generate_code()
		url: str = f"https://api.intra.42.fr/oauth/authorize?client_id={settings.OAUTH_CLIENT_UID}&redirect_uri={settings.OAUTH_REDIRECT_URI}&response_type=code&scope=public&state={self.state}'"
		return url

	@staticmethod
	def clear_cache(state: str):
		cache.delete(state)

	@staticmethod
	def request_for_token(state: str, code: str):
		data = {
			"grant_type": "authorization_code",
			"client_id": settings.OAUTH_CLIENT_UID,
			"client_secret": settings.OAUTH_CLIENT_SECRET,
			"code": code,
			"redirect_uri": settings.OAUTH_REDIRECT_URI,
			"state":  cache.get(state),
		}
		return requests.post(settings.OAUTH_TOKEN_URL, data=data)


	# @staticmethod
	# def get_user_info(token_data: dict):
	# 	email

	def __generate_code(self):
		code_verifier = "".join(random.choice(string.ascii_uppercase + string.digits) for _ in range(random.randint(43, 128)))
		self.state = hashlib.sha256(code_verifier.encode('utf-8')).digest()
		self.state = base64.urlsafe_b64encode(self.state).decode('utf-8').replace('=', '')
		cache.set(self.state, code_verifier, timeout=600)



