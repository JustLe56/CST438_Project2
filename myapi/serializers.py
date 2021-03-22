from rest_framework import serializers
from .models import WishListUser, Wishlist, WishlistItem, Link


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
        return Wishlist.objects.create(**validated_data)


class WishlistItemSerializer(serializers.ModelSerializer):

    link_url = serializers.URLField(source='link.url')

    def create(self, validated_data):
        link, created = Link.objects.get_or_create(url=validated_data.pop('link')['url'])
        return WishlistItem.objects.create(**validated_data, link=link)

    def update(self, instance, validated_data):
        link, created = Link.objects.get_or_create(url=validated_data.get('link', {'url': instance.link.url})['url'])
        instance.link = link
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.priority = validated_data.get('priority', instance.priority)
        instance.index = validated_data.get('index', instance.index)
        instance.save()
        return instance

    class Meta:
        model = WishlistItem
        exclude = ['id', 'link']
