from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import OrderViewSet,CartViewSet

router = DefaultRouter()

router.register(r'orders',OrderViewSet)
router.register(r'carts',CartViewSet)

urlpatterns = [
    path("/",include(router.urls))
]


