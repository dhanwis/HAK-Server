
from rest_framework import serializers
from .models import User, UserProfile


class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['phone_number']
        
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['phone_number'],**validated_data)
        user.is_customer = True
        user.save()
        return user



class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'
        extra_kwargs = {'user': {'read_only': True}}



