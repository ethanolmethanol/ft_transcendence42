import json
import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from shared_models.models import CustomUser

from .auth_helpers import get_session_from_request, perform_logout
from .oauth import OAuthBackend
from .serializers import UserSerializer

logger = logging.getLogger(__name__)


def login_user(request, username, password):
    user = authenticate(request, username=username, password=password)

    if user is not None:
        login(request, user)
        return True

    return False


@api_view(["POST"])
def signup(request):
    try:
        serializer = UserSerializer(data=request.data)

        if not serializer.is_valid():
            logger.error("Signup Error: %s", serializer.errors)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        serializer.save()
        # Access validated data directly from the serializer
        username = serializer.validated_data.get("username")
        password = serializer.validated_data.get("password")
        login_user(request, username, password)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    except IntegrityError as e:
        logger.error(json.dumps(e))
        return Response(json.dumps(e), status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
def signin(request):
    username = request.data.get("login")
    password = request.data.get("password")

    if login_user(request, username, password):
        response = Response(
            {"detail": "Successfully signed in."}, status=status.HTTP_200_OK
        )
        return response
    return Response(
        {"detail": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED
    )


@api_view(["POST"])
@csrf_protect
@login_required
def logout_view(request):
    try:
        # Assuming you want to perform some action before logging out
        get_session_from_request(request)
        # user_id = get_user_id(session) # be sure to uncomment the import when uncommenting this
        perform_logout(request)
        return Response(
            {"detail": "Successfully logged out."}, status=status.HTTP_200_OK
        )
    except ValueError as e:
        return Response(
            {"detail": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


@api_view(["GET"])
@csrf_protect
def is_logged_view(request):
    try:
        get_session_from_request(request)
        return Response({"detail": "User is logged in."}, status=status.HTTP_200_OK)
    except ValueError as e:
        return Response(
            {"detail": "User isn't logged in: " + str(e)},
            status=status.HTTP_401_UNAUTHORIZED,
        )


@api_view(["GET"])
def get_authorize_url(_):
    oauth_backend: OAuthBackend = OAuthBackend()
    return Response(oauth_backend.get_authorize_url())


@api_view(["POST"])
def exchange_code_for_user_id(request):
    state = request.data.get("state")
    code = request.data.get("code")

    if not code:
        return Response(
            {"error": "No code provided"}, status=status.HTTP_400_BAD_REQUEST
        )

    oauth_backend: OAuthBackend = OAuthBackend()
    response = oauth_backend.register_user(request, code, state)

    if response.status_code == status.HTTP_200_OK:
        return Response(
            data={
                "user_id": response.user_id,
                "new_user_created": response.new_user_created,
            },
            status=status.HTTP_200_OK,
        )
    return Response({"error": response.text}, status=response.status_code)


@api_view(["POST"])
def set_username_42(request):
    try:
        username, user_id = request.data.get("username"), request.data.get("user_id")

        if CustomUser.objects.filter(username=username).exists():
            return Response(
                {"error": "Username already taken."}, status=status.HTTP_400_BAD_REQUEST
            )

        user = CustomUser.objects.get(id=user_id)
        user.set_username(username)

        login(request, user)
        return Response({"success": True}, status=status.HTTP_200_OK)
    except KeyError:
        return Response(
            {"error": "Invalid request data."}, status=status.HTTP_400_BAD_REQUEST
        )
    except ObjectDoesNotExist:
        return Response(
            {"error": "User not found."}, status=status.HTTP_400_BAD_REQUEST
        )
