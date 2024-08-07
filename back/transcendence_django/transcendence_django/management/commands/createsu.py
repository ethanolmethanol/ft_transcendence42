from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
import os

class Command(BaseCommand):
	def handle(self, *args, **kwargs):
		if not User.objects.filter(username=os.environ['DJANGO_SUPERUSER_USERNAME']).exists():
			User.objects.create_superuser(
				username=os.environ['DJANGO_SUPERUSER_USERNAME'],
				email=os.environ['DJANGO_SUPERUSER_EMAIL'],
				password=os.environ['DJANGO_SUPERUSER_PASSWORD']
			)
