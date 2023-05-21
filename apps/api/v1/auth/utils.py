import secrets
from apps.users.models import User


def generate_unique_token(length=32):
    token = secrets.token_urlsafe(length)
    user = User.objects.filter(token=token).first()
    if user:
        return generate_unique_token(length=length)
    return token
