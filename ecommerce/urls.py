from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularSwaggerView,
    SpectacularRedocView,
)

urlpatterns = [
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(url_name="schema"),
        name="swagger-ui",
    ),
    path("api/redocs/", SpectacularRedocView.as_view(url_name="schema"), name="redocs"),
    path("api/auth/", include("users.urls")),
    # path('api/products/', include('products.urls')),
    # path('api/orders/', include('orders.urls')),
    # path('api/payments/', include('payments.urls')),
    # path('api/admin_panel/',include('admin_panel.urls')),
    # path('ws/',include('websockets.routing')),
    
]
