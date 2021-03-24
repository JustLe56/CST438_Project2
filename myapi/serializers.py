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
    class Meta:
        model = WishlistItem
        exclude = ['id', 'link']
        # wishlist field won't be used in creation or update, so it is read-only
        extra_kwargs = {'wishlist': {'read_only': True}}

    link_url = serializers.URLField(source='link.url')

    def __init__(self, *args, **kwargs):
        # if a "fields" kwarg is passed to the constructor, only those fields will be used by that instance
        fields = kwargs.pop('fields', None)

        super(WishlistItemSerializer, self).__init__(*args, **kwargs)

        if fields is not None:
            allowed = set(fields)
            existing = set(self.fields)
            for field_name in existing - allowed:
                self.fields.pop(field_name)

    def validate_index(self, value):
        # index is only validated in update operation, so it must equal an existing index
        wishlist_length = Wishlist.objects.get(wishlistUser=self.context['request'].user).wishlistitem_set.count()
        if value not in range(wishlist_length):
            raise serializers.ValidationError(
                "New index out of range, must be between 0 and %i inclusive" % (wishlist_length - 1)
            )
        return value

    def create(self, validated_data):
        validated_data['wishlist'] = Wishlist.objects.get(wishlistUser=self.context['request'].user)
        validated_data['link'], created = Link.objects.get_or_create(url=validated_data.pop('link')['url'])
        validated_data['index'] = validated_data['wishlist'].wishlistitem_set.count()
        return WishlistItem.objects.create(**validated_data)

    def update(self, instance, validated_data):
        # handle link updates
        link_url = validated_data.get('link', {'url': instance.link.url})['url']
        instance.link, created = Link.objects.get_or_create(url=link_url)
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.image_url = validated_data.get('image_url', instance.image_url)
        instance.priority = validated_data.get('priority', instance.priority)
        # handle index updates, assume index is in range(wishlist_length)
        new_index = validated_data.get('index', instance.index)
        if new_index != instance.index:
            original_index = instance.index
            # move item to the end
            instance.index = instance.wishlist.wishlistitem_set.count()
            instance.save()
            # decreasing the index means shifting items "forward"
            if new_index < original_index:
                for item_index in range(original_index - 1, new_index - 1, -1):
                    shifted_item = WishlistItem.objects.get(wishlist=instance.wishlist, index=item_index)
                    shifted_item.index += 1
                    shifted_item.save()
            # increasing the index means shifting items "backward"
            else:
                for item_index in range(original_index + 1, new_index + 1):
                    shifted_item = WishlistItem.objects.get(wishlist=instance.wishlist, index=item_index)
                    shifted_item.index -= 1
                    shifted_item.save()
            # move item to new_index
            instance.index = new_index
            instance.save()
        instance.save()
        return instance
