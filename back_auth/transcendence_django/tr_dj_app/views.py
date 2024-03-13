from django.contrib.auth import authenticate, login, get_user_model, logout
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import UserSerializer
from django.middleware.csrf import get_token

# import the logging library
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
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


from django.middleware.csrf import get_token


@api_view(['POST'])
def signin(request):
    user_login = request.data.get('login')
    password = request.data.get('password')
    logger.error("username/email: %s\npassword: %s" % (user_login.__str__(), password.__str__()))
    user = authenticate(request, login=user_login, password=password)
    if user is not None:
        login(request, user)
        # Get the CSRF token
        csrf_token = get_token(request)
        # Create a response
        response = Response({"detail": "Successfully signed in."}, status=status.HTTP_200_OK)
        # Set the CSRF token as a cookie in the response
        response.set_cookie('csrftoken', csrf_token)
        return response
    return Response({"detail": "Invalid username or password."}, status=status.HTTP_401_UNAUTHORIZED)


@api_view(['POST'])
def logout_view(request):
    try:
        logout(request)
        logger.info("User successfully logged out.")
        return Response({"detail": "Successfully logged out."}, status=200)
    except Exception as e:
        logger.error(f"Error logging out: {e}")
        return Response({"detail": "Error logging out."}, status=500)
