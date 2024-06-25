from rest_framework import serializers
from auth_app.models import User

class ProductAdminAddSerializers(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=["username",'phone_number','email','password','name']
        
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        user.is_product_admin = True
        user.save()
        return user  
        