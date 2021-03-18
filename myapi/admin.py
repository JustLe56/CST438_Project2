from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import WishListUserCreationForm, WishListUserChangeForm
from .models import WishListUser


class WishListUserAdmin(UserAdmin):
    add_form = WishListUserCreationForm
    form = WishListUserChangeForm
    model = WishListUser
    list_display = ['email', 'username', ]


admin.site.register(WishListUser, WishListUserAdmin)
