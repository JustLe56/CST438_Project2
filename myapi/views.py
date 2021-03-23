from rest_framework import generics
from .models import WishListUser
from .serializers import WishListUserSerializer
from .forms import WishListUserDeleteForm
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

@csrf_exempt
def delete_user_view(request):
    if request.user.is_authenticated:
        delete_form = WishListUserDeleteForm(instance=request.user)
        user = request.user
        user.delete()
        return JsonResponse({'detail': 'Account Successfully Deleted'})
    return JsonResponse({'detail': 'Not logged in'}, status=status.HTTP_400_BAD_REQUEST)
