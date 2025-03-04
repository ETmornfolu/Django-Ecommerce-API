from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet

router = DefaultRouter()

router.register(r"product", ProductViewSet)

urlpatterns = [path("/", include(router.urls))]
