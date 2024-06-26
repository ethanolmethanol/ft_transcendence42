# import the logging library
import logging
from http import HTTPStatus

from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_protect
from rest_framework.decorators import api_view
from rest_framework.response import Response

# Get an instance of a logger
logger = logging.getLogger(__name__)


@api_view(["GET"])
@csrf_protect
def user_data_view(request):
    # pylint: disable=no-member
    try:
        # Extract user ID from session data
        user_id = request.session.get("_auth_user_id")
        if user_id is None:
            return Response(
                {"detail": "User isn't logged in."}, status=HTTPStatus.UNAUTHORIZED
            )
        # Query the User model for the user with the given ID
        user = User.objects.get(pk=user_id)
        # Retrieve the user data
        user_data = {
            "id": user_id,
            "username": user.username,
            "email": user.email,
        }
        return Response(user_data, status=HTTPStatus.OK)
    except User.DoesNotExist:
        return Response({"detail": "User does not exist."}, status=HTTPStatus.NOT_FOUND)
