from rest_framework import viewsets
from core.permissions import IsSeller,IsBuyer,IsAdmin
from .models import Order,Cart
from .serializers import OrderSerializer,CartSerializer
from rest_framework.permissions import IsAuthenticated

class CartViewSet(viewsets.ModelViewSet):
    queryset=Cart.objects.all()
    permission_classes=[IsAuthenticated,IsBuyer]
    serializer_class=CartSerializer
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)


class OrderViewSet(viewsets.ModelViewSet):
    queryset=Order.objects.all()
    permission_classes=[IsAuthenticated,IsBuyer]
    serializer_class=OrderSerializer
    
    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)
    