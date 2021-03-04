from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from.models import wishListUser

class wishListUserCreationForm(UserCreationForm):

    class Meta:
        model = wishListUser
        fields = ('username', 'email')

class wishListUserChangeForm(UserChangeForm):

    class Meta:
        model = wishListUser
        fields = ('username', 'email')