from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from.models import WishListUser


class WishListUserCreationForm(UserCreationForm):

    class Meta:
        model = WishListUser
        fields = ('username', 'email')


class WishListUserChangeForm(UserChangeForm):

    class Meta:
        model = WishListUser
        fields = ('username', 'email')
