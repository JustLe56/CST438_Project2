from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import wishListUserCreationForm, wishListUserChangeForm
from .models import wishListUser

# Register your models here.

class wishListUserAdmin(UserAdmin):
    add_form = wishListUserCreationForm
    form = wishListUserChangeForm
    model = wishListUser
    list_display = ['email', 'username',]

admin.site.register(wishListUser, wishListUserAdmin)