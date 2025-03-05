import graphene
from graphene_django.types import DjangoObjectType
from .models import Product,Category


class CategoryType(DjangoObjectType):
    class Meta:
        model=Category
        fields=('id','name','description',)
        

class ProductType(DjangoObjectType):
    class Meta:
        model=Product
        fields=['id','name','description','price','stock','owner','category']
        
class Query(graphene.ObjectType):
    all_products=graphene.List(ProductType)
    product=graphene.Field(ProductType,id=graphene.Int())
    
    def resolve_all_products(self,info,**kwargs):
        return Product.objects.select_related('category').all()
    
    def resolve_product(self,info,id):
        return Product.objects.select_related('category').get(pk=id)

  
schema=graphene.Schema(query=Query)