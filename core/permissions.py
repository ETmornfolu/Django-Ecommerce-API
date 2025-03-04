from rest_framework.permissions import BasePermission

class IsBuyer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role=='buyer'

class IsSeller(BasePermission):
    def has_permission(self, request, view):
        # Only sellers can create products
        return request.user.role == 'seller'

    def has_object_permission(self, request, view, obj):
        # Only the owner (seller) can update or delete the product
        return obj.owner == request.user

class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role=='admin'

