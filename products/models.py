from django.db import models

from django.contrib.auth import get_user_model
from cloudinary.models import CloudinaryField

User=get_user_model()
# Create your models here.

class Category(models.Model):
    name=models.CharField(max_length=50)
    description=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name
    
    
class Product(models.Model):
    owner=models.ForeignKey(User,on_delete=models.CASCADE)
    name=models.CharField(max_length=200)
    description=models.TextField()
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products',null=True,blank=True)
    product_image=CloudinaryField('images',default='')
    price=models.DecimalField(max_digits=10,decimal_places=2)
    stock=models.IntegerField()
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    
    def __str__(self):
        return self.name