from django.urls import include, path
from .views import CreateWishListUser

urlpatterns = [
    path('createAccount/', CreateWishListUser.as_view()),
]
