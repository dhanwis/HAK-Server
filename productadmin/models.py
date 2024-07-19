from django.db import models
from decimal import Decimal

# Create your models here.

class Category(models.Model):
    image = models.ImageField(upload_to='category-image')
    name = models.CharField(max_length=50)

    def __str__(self) :
        return self.name
    

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True)
   

    def __str__(self):
        return self.name


class Size(models.Model):
    name = models.CharField(max_length=20)
    def __str__(self):
        return self.name


class ColorImage(models.Model):
    image = models.ImageField(upload_to='colorImg', null=True, blank=True)
    name = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return f"ColorImage {self.name}"


class Color(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=50)
    images = models.ManyToManyField(ColorImage, related_name='colors')

    def __str__(self):
        return self.name

    


class ProductVariant(models.Model):
    PRODUCT_STATUS_CHOICE = (("Sale", "Sale"),
                             ("Out of Stock", "Out of Stock"))
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    size = models.ForeignKey(Size, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    actual_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    discount_percentage = models.PositiveIntegerField(default=0)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    stock = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    
    class Meta:
        unique_together = ('product', 'size', 'color')

    def __str__(self):
        return f"{self.product.name} - {self.color} - {self.size}"
    
    def save(self, *args, **kwargs):
        if self.stock == 0 :
            self.product_status = "Out of Stock"
        else :
            self.product_status = "Sale"

        if self.actual_price and self.discount_percentage:
            discount_amount = (Decimal(self.discount_percentage) / 100) * self.actual_price
            self.discount_price = self.actual_price - discount_amount
        super().save(*args, **kwargs)
    
    