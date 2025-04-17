from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .serializers import ProductSerializer, CategorySerializer, ReviewSerializer
from .models import Product, Category, Review
from django_filters.rest_framework import DjangoFilterBackend, OrderingFilter
from core.permissions import IsSeller, IsAdmin, IsBuyer
from rest_framework.permissions import AllowAny


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsAuthenticated(), IsAdmin(), IsSeller()]
        return [AllowAny()]

#file
class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]  # Add filters
    filterset_fields = [
        "category",
    ]  # Fields to filter by
    # ordering_fields = ["created_at"]

    def get_queryset(self):
        queryset = Product.objects.all()
        if self.request.user.role == "seller":
            queryset = queryset.filter(owner=self.request.user)
        elif self.request.user.role == "admin":
            queryset = queryset
        return queryset.select_related("category").only(
            "id",
            "name",
            "description",
            "product_image",
            "price",
            "stock",
            "owner__username",
            "category__name",
        )

    def get_permissions(self):
        if self.request.method in ["POST", "PUT", "DELETE"]:
            return [IsAuthenticated(), IsSeller()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def update(self, request, *args, **kwargs):
        """Allow only sellers to update their products, and only admins to update verification_status."""
        product = self.get_object()

        if request.user.role == "seller":
            # Prevent sellers from modifying verification_status
            if "verification_status" in request.data:
                request.data.pop("verification_status")

            # Allow sellers to update their own products
            if product.owner != request.user:
                raise PermissionDenied("You can only update your own products.")

        elif request.user.role == "admin":
            # Admins can update verification_status, but they shouldn't edit other fields
            if len(request.data.keys()) == 1 and "verification_status" in request.data:
                return super().update(request, *args, **kwargs)
            else:
                raise PermissionDenied("Admins can only update verification status.")

        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Only product owners (sellers) can delete their products."""
        product = self.get_object()

        if product.owner != request.user:
            raise PermissionDenied("You do not have permission to delete this product.")

        return super().destroy(request, *args, **kwargs)


class ReviewVeiwSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated, IsBuyer]
