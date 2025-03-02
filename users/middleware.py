from django.utils.deprecation import MiddlewareMixin
from rest_framework_simplejwt.tokens import UntypedToken
from .models import UserProfile



class JWTAuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        access_token = request.COOKIES.get("access_token")

        if access_token:
            try:
                validated_token = UntypedToken(access_token)  # Validate JWT
                user_id = validated_token["user_id"]
                request.user = UserProfile.objects.get(id=user_id)
            except Exception:
                request.user = None  # If token is invalid, don't authenticate
