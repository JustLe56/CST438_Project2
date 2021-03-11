from rest_framework import serializers
from .models import WishListUser


class WishListUserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = WishListUser
        fields = ['username', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = WishListUser(**validated_data)
        user.set_password(password)
        user.save()
        return user
