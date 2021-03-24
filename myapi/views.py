from rest_framework import generics, mixins, permissions
from .models import WishListUser, WishlistItem, Wishlist
from .serializers import WishListUserSerializer, WishlistItemSerializer
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
import json


class CreateWishListUser(generics.CreateAPIView):
    queryset = WishListUser.objects.all()
    serializer_class = WishListUserSerializer
    http_method_names = (u'post', u'options')


class CreateWishlistItem(generics.CreateAPIView):
    serializer_class = WishlistItemSerializer
    http_method_names = (u'post', u'options')
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.get(wishlistUser=self.request.user).wishlistitem_set

    def get_serializer(self, *args, **kwargs):
        kwargs['fields'] = ['link_url', 'name', 'description', 'image_url', 'priority']
        return super().get_serializer(*args, **kwargs)


class RetrieveUpdateDestroyWishlistItem(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = WishlistItemSerializer
    http_method_names = (u'get', u'put', u'patch', u'delete', u'options')
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'index'

    def get_queryset(self):
        return Wishlist.objects.get(wishlistUser=self.request.user).wishlistitem_set

    def perform_destroy(self, instance):
        wishlist_length = instance.wishlist.wishlistitem_set.count()
        instance_index = instance.index
        wishlist = instance.wishlist
        instance.delete()
        # shift other items back
        for item_index in range(instance_index, wishlist_length - 1):
            item = WishlistItem.objects.get(wishlist=wishlist, index=item_index + 1)
            item.index -= 1
            item.save()


class RetrieveWishlistItemList(generics.ListAPIView):
    serializer_class = WishlistItemSerializer
    http_method_names = (u'get', u'options')
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Wishlist.objects.get(wishlistUser=self.request.user).wishlistitem_set


@csrf_exempt
@require_POST
def api_login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    if username is None or password is None:
        return JsonResponse(
            {"errors": {"__all__": "Please enter both username and password"}},
            status=status.HTTP_400_BAD_REQUEST
        )
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({'detail': 'Success'})
    return JsonResponse({'detail': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def api_logout_view(request):
    if request.user.is_authenticated:
        logout(request)
        return JsonResponse({'detail': 'Success'})
    return JsonResponse({'detail': 'Not logged in'}, status=status.HTTP_400_BAD_REQUEST)
