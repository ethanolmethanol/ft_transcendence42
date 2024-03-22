from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import status

from .auth_helpers import get_session_from_request, get_user_id, perform_logout
from .serializers import UserSerializer
from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response

# import the logging library
import logging

# import libraries for username and email availability checks

# Get an instance of a logger
logger = logging.getLogger(__name__)


# SignUp


@api_view(['POST'])
def signup(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        # Access validated data directly from the serializer
        username = serializer.validated_data.get('username')
        email = serializer.validated_data.get('email')
        password = serializer.validated_data.get('password')
        logger.error("username: %s\nemail: %s\npassword: %s" % (username, email, password))
        # User.objects.create_user(username='newuser', password='password')
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    else:
        logger.error("Signup Error: %s" % serializer.errors)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# SignIn


@api_view(['POST'])
def signin(request):
    user_login = request.data.get('login')
    password = request.data.get('password')
    logger.error("username/email: %s\npassword: %s" % (user_login.__str__(), password.__str__()))
    user = authenticate(request, login=user_login, password=password)
    if user is not None:
        login(request, user)
        response = Response({"detail": "Successfully signed in."}, status=status.HTTP_200_OK)
        return response
    return Response({"detail": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)


# Logout


# def get_session_id(request):
#     session_id = request.COOKIES.get('sessionid')
#     if not session_id:
#         logger.error("Session ID is missing.")
#         raise ValueError("Session ID is missing!")
#     return session_id


# def get_session(session_id):
#     try:
#         session = Session.objects.get(session_key=session_id)
#     except ObjectDoesNotExist:
#         logger.error("Invalid session ID.")
#         raise ValueError("Invalid session ID.")
#     return session
#
#
# def get_user_id(session):
#     user_id = session.get_decoded().get('_auth_user_id')
#     if not user_id:
#         logger.error("User not authenticated.")
#         raise ValueError("User not authenticated.")
#     return user_id
#
#
# def perform_logout(request):
#     try:
#         logout(request)
#         logger.info("User successfully logged out.")
#     except Exception as e:
#         logger.error(f"Error logging out: {e}")
#         raise ValueError("Error logging out.")
#
#
# def get_csrf(request):
#     csrf = request.META.get('HTTP_X_CSRFTOKEN')
#     if not csrf:
#         logger.error("Csrf Token is missing.")
#         raise ValueError("Csrf Token is missing!")
#     return csrf
#
#
# def get_session_from_request(request):
#     session_id = get_session_id(request)
#     return get_session(session_id)


@api_view(['POST'])
@csrf_protect
@login_required
def logout_view(request):
    try:
        # Assuming you want to perform some action before logging out
        session = get_session_from_request(request)
        user_id = get_user_id(session)
        perform_logout(request)
        return Response({"detail": "Successfully logged out."}, status=200)
    except ValueError as e:
        return Response({"detail": str(e)}, status=500)


# Is logged

@api_view(['GET'])
@csrf_protect
def is_logged_view(request):
    try:
        get_session_from_request(request)
        return Response({"detail": "User is logged in."}, status=200)
    except Exception as e:
        return Response({"detail": "User isn't logged in: " + str(e)}, status=status.HTTP_401_UNAUTHORIZED)
