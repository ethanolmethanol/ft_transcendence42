from django.contrib.auth import authenticate, login, get_user_model, logout
from django.views.decorators.csrf import csrf_protect, ensure_csrf_cookie
from rest_framework import status
from .serializers import UserSerializer

# import the logging library
import logging
#import libraries for username and email availability checks
from django.http import JsonResponse
from django.contrib.auth.models import User


from django.contrib.auth import logout
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.decorators import api_view
from rest_framework.response import Response
import logging

# Get an instance of a logger
logger = logging.getLogger(__name__)


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


from django.middleware.csrf import get_token


@api_view(['POST'])
@ensure_csrf_cookie
def signin(request):
    user_login = request.data.get('login')
    password = request.data.get('password')
    logger.error("username/email: %s\npassword: %s" % (user_login.__str__(), password.__str__()))
    user = authenticate(request, login=user_login, password=password)
    if user is not None:
        login(request, user)
        # Get the session ID
        session_id = request.session.session_key
        # Get the csrf_token
        csrf_token = get_token(request)
        # Create a response
        response = Response({"detail": "Successfully signed in.", "sessionId": session_id, "csrfToken": csrf_token}, status=status.HTTP_200_OK)
        return response
    return Response({"detail": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)


logger = logging.getLogger(__name__)

@api_view(['POST'])
# @csrf_protect
def logout_view(request):
    # Extract the session ID from the request headers
    logger.error(f"Request headers: {request.META}")
    session_id = request.META.get('HTTP_X_SESSION_ID')
    if not session_id:
        logger.error("Session ID is missing.")
        return Response({"detail": "Session ID is missing!"}, status=400)

    try:
        # Attempt to load the session using the provided session ID
        session = Session.objects.get(session_key=session_id)
    except ObjectDoesNotExist:
        logger.error("Invalid session ID.")
        return Response({"detail": "Invalid session ID."}, status=401)

    # Check if the session is associated with an authenticated user
    user_id = session.get_decoded().get('_auth_user_id')
    if not user_id:
        logger.error("User not authenticated.")
        return Response({"detail": "User not authenticated."}, status=401)

    try:
        # Proceed with the logout operation
        logout(request)
        logger.info("User successfully logged out.")
        return Response({"detail": "Successfully logged out."}, status=200)
    except Exception as e:
        logger.error(f"Error logging out: {e}")
        return Response({"detail": "Error logging out."}, status=500)
