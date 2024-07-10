from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        Model=Category
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
    class Meta:
        model=ColorImage
        fields="__all__"



class ColorSerializer(serializers.ModelSerializer):
    images = ColorImageSerializer(many=True)
    class Meta:
        model=Color
        fields="__all__"


class ProductvarientSerializer(serializers.ModelSerializer):
    class Meta:
        model=ProductVariant
        fields="__all__"