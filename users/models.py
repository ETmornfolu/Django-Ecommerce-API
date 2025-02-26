from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
    Group,
    Permission,
)
from cloudinary.models import CloudinaryField


# Create your models here.


class CustomUserManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError("Email Field is requried")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", "admin")
        return self.create_user(email, username, **extra_fields)


class UserProfile(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ("buyer", "Buyer"),
        ("seller", "Seller"),
        ("admin", "Admin"),
    ]
    email = models.EmailField(unique=True)
    username = models.CharField(unique=True, max_length=30)
    first_name = models.CharField(max_length=40)
    last_name = models.CharField(max_length=40)
    phone_no = models.CharField(unique=True, max_length=12, null=True, blank=True)
    address = models.TextField(null=True, blank=True)
    nationality = models.CharField(null=True, blank=True, max_length=30)
    avatar = CloudinaryField("images", default="")
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default="buyer")
    date_joined = models.DateTimeField(auto_now_add=True)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Fix conflicts with Django’s built-in User model
    groups = models.ManyToManyField(
        Group, related_name="ecommerce_users_groups", blank=True
    )
    user_permissions = models.ManyToManyField(
        Permission, related_name="ecommerce_users_permissions", blank=True
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.email
