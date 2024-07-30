from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model=Category
        fields="__all__"
        
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model=Product
        fields="__all__"
        
        
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Size
        fields="__all__"
        


class ColorImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = ColorImage
        fields = '__all__'

    def get_image_url(self, obj):
        if obj.image:
            return obj.image.url
        return ""

class ColorSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Color
        fields = '__all__'

    def get_image_url(self, obj):
        if obj.image and obj.image.image:
            return obj.image.image.url
        return ""


class ProductvarientSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductVariant
        fields="__all__"

class ProductDisplaySerializer(serializers.ModelSerializer):
    color = ColorSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    size = SizeSerializer(read_only=True)
    category = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ['id', 'category', 'product', 'size', 'color', 'actual_price', 'discount_price', 'stock', 'product_status']

    def get_category(self, obj):
        category = obj.product.category
        return CategorySerializer(category).data