# import the logging library
import logging

from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .oauth import OAuthBackend
from shared_models.models import CustomUser

# get_user_id,
from .auth_helpers import get_session_from_request, perform_logout
from .serializers import UserSerializer

# import libraries for username and email availability checks

# import libraries for username and email availability checks

# Get an instance of a logger
logger = logging.getLogger(__name__)
# SignUp

def authenticate_user(request, username, password) -> bool:
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return True
    return False


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
def exchange_code_for_user_id(request):
    state = request.data.get('state')
    code = request.data.get('code')

    logger.info(f"code: {code}")
    if not code:
        logger.error(f"code is empty")
        return Response({"error": "No code provided"}, status=400)

    oauth_backend: OAuthBackend = OAuthBackend()
    response = oauth_backend.register_user(request, code, state)

    logger.info(f"response: {response}")
    if response.status_code == 200:
        logger.info(f"user_id: {response.user_id}")
        return Response(data={
            "user_id": response.user_id,
            "new_user_created": response.new_user_created,
        }, status=status.HTTP_200_OK)
    else:
        logger.error(f"error : {response.text}")
        return Response({"error": response.text}, status=response.status_code)


@api_view(["POST"])
def set_username_42(request):
    username, user_id = request.data.get('username'), request.data.get('user_id')

    try:
        if CustomUser.objects.filter(username=username).exists():
            return Response({"error": "Username already taken."}, status=400)

        user = CustomUser.objects.get(id=user_id)
        user.username = username
        user.save()

        login(request, user)
        return Response({"success": True}, status=status.HTTP_200_OK)

    except CustomUser.DoesNotExist:
        return Response({"error": "User not found."}, status=404)