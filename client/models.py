from django.db import models
from auth_app.models import *
from productadmin.models import *
import random   
# Create your models here.

class CartItem(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_superuser': False, 'is_product_admin': False})
    item = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    is_ordered = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.phone_number}'s cart item: {self.item.product.name} - {self.quantity}"

    @property
    def total_price(self):
        return self.quantity * self.item.discount_price

class WishList(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_superuser': False, 'is_product_admin': False})
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.product.product.name}"
    
class CheckOut(models.Model) :
    STATUS_CHOICE = (
        ("Order Pending", "Order Pending"),
        ("Order Confirmed", "Order Confirmed"),
        ("Order Shipped", "Order Order Shipped"),
        ("Order Delivered", "Order Delivered")
    )
    order_status = models.CharField(max_length=20, choices=STATUS_CHOICE, default="Order Pending")
    id = models.CharField(max_length=4, primary_key=True)
    order = models.ForeignKey(CartItem, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.TextField()
    mobile_no = models.CharField(max_length=10)
    company_name = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)

    def save(self, *args, **kwargs):
        if not self.id:
            self.id = self.generate_unique_id()
        super(CheckOut, self).save(*args, **kwargs)

    def generate_unique_id(self):
        check_id = str(random.randint(1000, 9999))
        while CheckOut.objects.filter(id=check_id).exists():
            check_id = str(random.randint(1000, 9999))
        return check_id
    
    def __str__(self) :
        return f"{self.id} - {self.first_name} - {self.order_status}"

class Review(models.Model) :
    user = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_superuser': False, 'is_product_admin': False})
    product = models.ForeignKey(ProductVariant, on_delete=models.CASCADE)
    description = models.TextField()

