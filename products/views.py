from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer,CategorySerializer
from .models import Product,Category
from django_filters.rest_framework import DjangoFilterBackend,OrderingFilter
from core.permissions import IsSeller,IsAdmin,IsBuyer

class CategoryViewSet(viewsets.ModelViewSet):
    queryset=Category.objects.all()
    serializer_class=CategorySerializer
    permission_classes=[IsAuthenticated]


class ProductViewSet(viewsets.ModelViewSet):
    queryset=Product.objects.all()
    serializer_class=ProductSerializer
    permission_classes=[IsAuthenticated,IsSeller]
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["category", "created_at"]
    ordering_fields = ["created_at"]
    
    
    def get_queryset(self):
        queryset=Product.objects.all()
        if self.request.user.role == 'seller':
            queryset.filter(owner=self.request.user)
        elif self.request.user.role=='admin':
            queryset=queryset
        return queryset.select_related('category').only('id','name','description','product_image','price','stock','owner__username','category__name')