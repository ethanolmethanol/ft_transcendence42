# import the logging library
import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from oauth2_provider.contrib.rest_framework import OAuth2Authentication
from rest_framework.permissions import IsAuthenticated

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
