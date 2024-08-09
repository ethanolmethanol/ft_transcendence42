# import the logging library
import logging
import os

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated
from .oauth import OAuthBackend
from django.conf import settings
from django.shortcuts import redirect
import requests

# get_user_id,
from .auth_helpers import get_session_from_request, perform_logout
from .serializers import UserSerializer

# import libraries for username and email availability checks

# import libraries for username and email availability checks

# Get an instance of a logger
logger = logging.getLogger(__name__)
# SignUp


@api_view(["POST"])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # Access validated data directly from the serializer
        username = serializer.validated_data.get("username")
        email = serializer.validated_data.get("email")
        password = serializer.validated_data.get("password")
        logger.error("username: %s\nemail: %s\npassword: %s", username, email, password)
        # User.objects.create_user(username='newuser', password='password')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    logger.error("Signup Error: %s", serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# SignIn


@api_view(["POST"])
def signin(request):
    user_login = request.data.get("login")
    password = request.data.get("password")
    user = authenticate(request, username=user_login, password=password)
    if user is not None:
        login(request, user)
        response = Response(
            {"detail": "Successfully signed in."}, status=status.HTTP_200_OK
        )
        return response
    return Response(
        {"detail": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED
    )

@api_view(["POST"])
def oauth2(request):
    pass

# Logout

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


# Is logged


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
def get_authorize_url(request):
    oauth_backend: OAuthBackend = OAuthBackend()
    return Response(oauth_backend.get_authorize_url())


@api_view(["POST"])
def exchange_code(request):
    state = request.data.get('state')
    code = request.data.get('code')

    if not code:
        logger.error("No code provided")
        return Response({"error": "No code provided"}, status=400)

    logger.info(f"Exchanging code: {code}")
    response = OAuthBackend.request_for_token(state, code)

    logger.info(f"Exchanging token: {response}")
    if response.status_code == 200:
        OAuthBackend.clear_cache(state)
        token_data = response.json()
        logger.info("Token data: %s", token_data)
        # username, email = OAuthBackend.get_user_info(token_data)
        return Response(token_data)
    else:
        logger.error("Failed to exchange code, error: %s", response.text)
        return Response({"error": "Failed to exchange code for token"}, status=response.status_code)