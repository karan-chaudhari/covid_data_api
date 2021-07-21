from rest_framework import serializers
from .models import UserProfile

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email','password','country')

# Signup Serializer
class SignupSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('first_name', 'last_name', 'email','password','country')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = UserProfile.objects.create(first_name=validated_data['first_name'], last_name=validated_data['last_name'],email=validated_data['email'], password=validated_data['password'], country=validated_data['country'])

        return user