import logging

from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session
from django.core.exceptions import ObjectDoesNotExist

logger = logging.getLogger(__name__)


def get_session_id(request):
    session_id = request.COOKIES.get("sessionid")
    if not session_id:
        logger.error("Session ID is missing.")
        raise ValueError("Session ID is missing!")
    return session_id


def get_session(session_id):
    try:
        session = Session.objects.get(session_key=session_id)
    except ObjectDoesNotExist as exc:
        logger.error("Invalid session ID.")
        raise ValueError("Invalid session ID.") from exc
    return session


def get_user_id(session):
    user_id = session.get_decoded().get("_auth_user_id")
    if not user_id:
        logger.error("User not authenticated.")
        raise ValueError("User not authenticated.")
    return user_id


def perform_login(request, username, password):
    user = authenticate(request, username=username, password=password)

    if user is not None:
        # pylint: disable=no-member
        user.login_user(request)  # type: ignore[attr-defined]
        return True

    return False


def perform_logout(request):
    get_session_from_request(request)
    try:
        user = request.user
        user.logout_user(request)
        logger.info("User successfully logged out.")
    except Exception as e:
        logger.error("Error logging out: %s", e)
        raise ValueError("Error logging out.") from e


def get_csrf(request):
    csrf = request.META.get("HTTP_X_CSRFTOKEN")
    if not csrf:
        logger.error("Csrf Token is missing.")
        raise ValueError("Csrf Token is missing!")
    logger.info("Csrf Token was successfully retrieved.")
    return csrf


def get_session_from_request(request):
    session_id = get_session_id(request)
    return get_session(session_id)
