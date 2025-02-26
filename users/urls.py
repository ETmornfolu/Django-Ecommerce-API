from django.urls import path, include
from .views import (
    LoginView,
    RegisterView,
    UserViewset,
    ResetPasswordView,
    ConfirmResetPassswordView,
    LogoutView,
)
from rest_framework.routers import DefaultRouter

router = DefaultRouter()
router.register(r"users", UserViewset, basename="users")

urlpatterns = [
    path("register/", RegisterView.as_view(), name="user-register"),
    path("login/", LoginView.as_view(), name="user-login"),
    path("logout/", LogoutView.as_view(), name="user-logout"),
    path("password-rest/", ResetPasswordView.as_view(), name="user-password-reset"),
    path(
        "password-reset-confirm/<uidb64>/<token>/",
        ConfirmResetPassswordView.as_view(),
        name="user-password-reset-confirm",
    ),
    path("", include(router.urls)),
]
