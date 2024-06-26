from rest_framework import serializers
from .models import *

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        Model=Category
        fields="__all__"
        
        
class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        models=Product
        fields="__all__"
        
        
class SizeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Size
        fields="__all__"
        


class ColorImageSerializer(serializers.ModelSerializer):
    class Meta:
        model=ColorImage
        fields="__all__"