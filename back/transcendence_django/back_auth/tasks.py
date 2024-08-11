import logging
from celery import shared_task
from datetime import timedelta
from django.utils import timezone
import requests
from shared_models.models import OauthToken
from django.conf import settings


logger = logging.getLogger(__name__)


@shared_task
def refresh_tokens():
	tokens = OauthToken.objects.all()
	for token in tokens:
		if token.token_expires_at <= timezone.now() + timedelta(minutes=5):
			new_token_data = refresh_the_token(token.refresh_token)
			if new_token_data:
				token.store_tokens(new_token_data)
				logger.info(f"Token refreshed successfully for {token.id}")
			else:
				logger.error(f"Failed to refresh token for {token.id}")


def refresh_the_token(refresh_token):
	try:
		response = requests.post(settings.OAUTH_TOKEN_URL, data={
			"grant_type": "refresh_token",
			"refresh_token": refresh_token,
			"client_id": settings.OAUTH_CLIENT_UID,
			"client_secret": settings.OAUTH_CLIENT_SECRET,
		})

		if response.status_code == 200:
			return response.json()
		else:
			logger.error(f"Failed to refresh token: {response.status_code} {response.text}")
			return None
	except requests.RequestException as e:
		logger.error(f"Exception occurred while refreshing token: {str(e)}")
		return None
