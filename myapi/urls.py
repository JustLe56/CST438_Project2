from django.urls import path
from .views import (CreateWishListUser, api_login_view, api_logout_view, RetrieveUpdateDestroyWishlistItem,
                    CreateWishlistItem, RetrieveWishlistItemList, delete_user_view)
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('createAccount/', CreateWishListUser.as_view()),
    path('login/', api_login_view),
    path('logout/', api_logout_view),
    path('deleteUser/', delete_user_view),
    path('item/', CreateWishlistItem.as_view()),
    path('item/<int:index>', RetrieveUpdateDestroyWishlistItem.as_view()),
    path('listitems/', RetrieveWishlistItemList.as_view())
]

urlpatterns = format_suffix_patterns(urlpatterns)
