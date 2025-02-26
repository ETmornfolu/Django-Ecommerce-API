from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.decorators import action
# from rest_framework.generics import GenericAPIView, CreateAPIView
from rest_framework import viewsets
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from .models import UserProfile
from .serializers import (
    UserSerializer,
    RegisterSerializer,
    LoginSerializer,
    PasswordResetSerializer,
    UpdateUserSerializer,
    
)
from core.permissions import IsAdmin, IsBuyer, IsSeller
from rest_framework.permissions import IsAuthenticated, IsAdminUser,AllowAny
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.filters import OrderingFilter
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.conf import settings
from celery_tasks.tasks import send_email_reset_password
from drf_spectacular.utils import extend_schema,OpenApiParameter


# Create your views here.


class UserViewset(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated,IsAdminUser]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["role", "nationality"]
    ordering_fields = ["date_joined", "email"]
    
    def get_queryset(self):
        return UserProfile.objects.all().only('id','email','first_name','last_name','role')
    
    @action(detail=False, methods=["get"], permission_classes=[IsAuthenticated])
    def user(self, request):
        serializer=self.get_serializer(request.user)
        return Response(serializer.data)

# class UpdateUserviewSet(viewsets.ModelViewSet):
#     serializer_class=UpdateUserSerializer
#     permission_classes=[IsAuthenticate
      


class RegisterView(APIView):
    seriailzer_class=RegisterSerializer
    permission_classes=[AllowAny]
    
    @extend_schema(request=RegisterSerializer,responses={200: None})
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_201_CREATED,
            )
        
        print("❌ Serializer Errors:", serializer.errors)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class=LoginSerializer
    permission_classes=[AllowAny]
    
    @extend_schema(request=LoginSerializer,responses={200:None})
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data
            refresh = RefreshToken.for_user(user)
            return Response(
                {"refresh": str(refresh), "access": str(refresh.access_token)},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LogoutView(APIView):
    
    @extend_schema(exclude=True)
    def post(self, request):
        try:
            refresh_token = request.data["refresh"]
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as e:
            return Response(status=status.HTTP_404_NOT_FOUND)


def generate_reset_link(user):
    uid = urlsafe_base64_encode(force_bytes(user.pk))
    token = default_token_generator.make_token(user)
    return f"{settings.FRONTEND_URL}/reset-passsword-confirm/{uid}/{token}"


class ResetPasswordView(APIView):
    serializer_class=PasswordResetSerializer
    
    @extend_schema(request=PasswordResetSerializer,responses={200:None})
    def post(self, request):
        serializer = PasswordResetSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data["email"]
            user = UserProfile.objects.filter(email=email)

            reset_link = generate_reset_link(user)
            send_email_reset_password.delay(email, reset_link)
            return Response(
                {"message": "Password reset mail has been sent"},
                status=status.HTTP_200_OK,
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ConfirmResetPassswordView(APIView):
    
    @extend_schema(
        parameters=[
            OpenApiParameter(name='uidb64', type=str, location=OpenApiParameter.PATH),
            OpenApiParameter(name='token', type=str, location=OpenApiParameter.PATH),
        ]
    )
    def post(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = UserProfile.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, UserProfile.DoesNotExist):
            user = None

        if user and default_token_generator.check_token(user, token):
            new_password = request.data.get("new_password")

            user.set_password(new_password)
            user.save()
            return Response(
                {"message": "Password has been changed successfully "},
                status=status.HTTP_200_OK,
            )
        return Response(
            {"message": "Invalid token"}, status=status.HTTP_401_UNAUTHORIZED
        )
