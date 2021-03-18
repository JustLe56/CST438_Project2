from django.urls import path
from .views import CreateWishListUser, api_login_view

urlpatterns = [
    path('createAccount/', CreateWishListUser.as_view()),
    path('login/', api_login_view),
    path('logout/' api_logout_view)
]
