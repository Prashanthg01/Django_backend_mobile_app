from rest_framework import serializers
from .models import MyUser

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = MyUser
        fields = ('id', 'UserID', 'name', 'phone_number', 'email', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = MyUser.objects.create_user(
            UserID=validated_data['UserID'],
            password=validated_data['password'],
            name=validated_data['name'],
            phone_number=validated_data['phone_number'],
            email=validated_data['email']
        )
        return user
