from datetime import datetime
from django.http import HttpResponse
from django.conf import settings


def set_auth_cookie(response: HttpResponse, key: str, value: str, expiry_time):
    response.set_cookie(
        key=key,
        value=value,
        httponly=True,
        secure=settings.SIMPLE_JWT["AUTH_COOKIE_SECURE"],
        samesite=settings.SIMPLE_JWT["AUTH_COOKIE_SAMESITE"],
        expires=datetime.utcnow()
        + expiry_time,
    )
