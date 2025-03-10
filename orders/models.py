from django.db import models
from products.models import Product
from django.contrib.auth import get_user_model

User=get_user_model()

# Create your models here.


class Order(models.Model):
    STATUS_CHOICES={
        ('pending','Pending'),
        ('processing','Processing'),
        ('shipped','Shipped'),
        ('delivered','Delivered'),
        ('cancelled','Cancelled')
    }
    user=models.ForeignKey(User,on_delete=models.CASCADE,related_name='orders')
    status=models.CharField(max_length=20,choices=STATUS_CHOICES,default='pending')
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering=['-created_at']
        
    def __str__(self):
        return f"{self.user.username}'s Orders "
    
class OrderItem(models.Model):
    order=models.ForeignKey(Order,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='order_items')
    quantity=models.PositiveIntegerField()
    price=models.DecimalField(max_digits=10,decimal_places=2)
    
    def __str__(self):
        return f"{self.order.user.username}--- {self.product.name}"

class Cart(models.Model):
    user=models.OneToOneField(User, on_delete=models.CASCADE,related_name='cart')
    

class CartItem(models.Model):
    cart=models.ForeignKey(Cart,on_delete=models.CASCADE,related_name='items')
    product=models.ForeignKey(Product,on_delete=models.CASCADE,related_name='cart_items')
    quantity=models.PositiveIntegerField()
    
