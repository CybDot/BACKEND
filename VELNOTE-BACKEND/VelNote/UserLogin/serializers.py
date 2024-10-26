from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'password', 'username', 'first_name', 'last_name']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            username=validated_data['username'], 
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', ''),
        )
        user.set_password(validated_data['password'])  
        user.save()
        return user

class UserLoginSerializer(serializers.Serializer):
    email = serializers.CharField()  
    password = serializers.CharField(write_only=True)


