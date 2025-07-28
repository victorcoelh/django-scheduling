from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken

from api.tasks import send_welcome_email
from api.utils.types import JwtTokens


def register_service(user: User) -> JwtTokens:
    """Handles registration tasks for a new user, including sending a welcome email 
    and issuing JWT tokens for authentication. The welcome e-mail is sent asynchronously
    using a Celery shared task.

    Args:
        user (User): A Django User Model instance representing the newly registered user.

    Returns:
        JwtTokens: A TypedDict containing the access and  refresh tokens for the user session.
    """
    send_welcome_email.delay(user.email) # pyright: ignore[reportFunctionMemberAccess]
    tokens = authentication_service(user)
    return tokens

def authentication_service(user: User) -> JwtTokens:
    """Generates JWT access and refresh tokens for the given user.
    Uses `django_simplejwt`'s `RefreshToken` to create the token pair.

    Args:
        user (User): The Django user to authenticate.

    Returns:
        JwtTokens: A TypedDict containing the access and refresh tokens for the user session.
    """
    tokens = RefreshToken.for_user(user)
    tokens = JwtTokens(access=str(tokens.access_token),refresh=str(tokens))
    return tokens
