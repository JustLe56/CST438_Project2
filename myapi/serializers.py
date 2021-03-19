from rest_framework import serializers
from .models import WishListUser, Wishlist


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
        # Create user's personal wishlist
        WishlistSerializer().create({'wishlistUser': user})
        return user


class WishlistSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Wishlist
        fields = '__all__'

    def create(self, validated_data):
        wishlist = Wishlist(**validated_data)
        wishlist.save()
        return wishlist
