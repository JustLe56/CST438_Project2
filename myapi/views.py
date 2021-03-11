from rest_framework import generics
from .models import WishListUser
from .serializers import WishListUserSerializer


class CreateWishListUser(generics.CreateAPIView):
    queryset = WishListUser.objects.all()
    serializer_class = WishListUserSerializer
    http_method_names = (u'post', u'options')
