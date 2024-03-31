# import the logging library
import logging

from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Get an instance of a logger
logger = logging.getLogger(__name__)


@api_view(["GET"])
@csrf_protect
def username_view(request):
    try:
        # Extract user ID from session data
        user_id = request.session.get("_auth_user_id")
        if user_id is None:
            return Response({"detail": "User isn't logged in."}, status=401)
        # Query the User model for the user with the given ID
        user = get_user_model().objects.get(pk=user_id)
        # Retrieve the username
        username = user.username
        return Response({"username": username}, status=200)
    except get_user_model().DoesNotExist:
        return Response({"detail": "User does not exist."}, status=404)