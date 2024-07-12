from rest_framework import serializers
from auth_app.models import User ,UserProfile

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
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}


class OrderAdminProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
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