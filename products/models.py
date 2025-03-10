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
    PRODUCT_STATUS=[
        ('unverified','Unverified'),
        ('pending','Pending'),
        ('verified','Verified'),
    ]
    name=models.CharField(max_length=150,unique=True)
    owner=models.ForeignKey(User,on_delete=models.CASCADE,related_name='products',null=True,blank=True)
    description=models.TextField()
    product_image=CloudinaryField('images',default='default_img',null=True,blank=True)
    price=models.DecimalField(max_digits=10,decimal_places=2)
    category=models.ForeignKey(Category,on_delete=models.CASCADE,related_name='products',null=True,blank=True)
    stock=models.PositiveIntegerField()
    verification_status=models.CharField(max_length=15,choices=PRODUCT_STATUS,default='pending')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['-created_at']
        indexes=[
            models.Index(fields=['name']),
            models.Index(fields=['price'])
        ]
    def __str__(self):
        return self.name
    
    

class Review(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='reviews')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='reviews')
    rating=models.PositiveIntegerField()
    comment=models.TextField()
    created_at=models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together=('user','product')
        ordering=['-created_at']
    