from rest_framework import serializers
from auth_app.models import User ,UserProfile
from client.models import CheckOut

class ProductAdminAddSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username",'phone_number','email','password','name']
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_product_admin = True
        user.save()
        return user  
        

class ProductAdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id","username",'phone_number','email','name','is_product_admin']
        extra_kwargs = {'user': {'read_only': True}}

class OrderAdminAddSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username",'phone_number','email','password','name']
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_order_admin = True
        user.save()
        return user  


class OrderAdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username",'phone_number','email','name','is_order_admin']
        extra_kwargs = {'user': {'read_only': True}}

class SalesAdminAddSerializer(serializers.ModelSerializer) :
    class Meta:
        model=User
        fields=["username",'phone_number','email','password','name']

    def create(self, validate_data) :
        user = User.objects.create_user(**validate_data)
        user.is_sales_admin = True
        user.save()
        return user

class SalesAdminProfileSerializer(serializers.ModelSerializer) :
    class Meta:
        model=User
        fields=fields=["username",'phone_number','email','name','is_sales_admin']
        extra_kwargs = {'user': {'read_only': True}}

class OrderStatusChangeSerializer(serializers.ModelSerializer) :
    class Meta:
        model=CheckOut
        fields=['order_status']