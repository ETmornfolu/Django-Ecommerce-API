from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet
from graphene_django.views import GraphQLView
from .schema import schema

router = DefaultRouter()

router.register(r"product", ProductViewSet)
router.register(r"category",CategoryViewSet)

urlpatterns = [
    path("/", include(router.urls)),
    path("graphql/", GraphQLView.as_view(graphiql=True, schema=schema)),
]
