from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST, require_GET
import json

@csrf_exempt
@require_POST
def load_items(request):
    data = json.loads(request.body)
    request.session['items'] = (sorted(data, key=lambda i: (i['priority'], i['name'])))
    return JsonResponse({'detail': "items_loaded"})


def logout_usr(request):
    logout(request)
    return HttpResponseRedirect('/login')


def home(request):
    if 'items' not in request.session:
        request.session['items'] = list()
    context = {}
    user = request.user
    if user.is_authenticated:
        return render(request, '../templates/home.html', context)
    return redirect('/login')


def createAcc(request):
    context = {}
    return render(request, '../templates/createAcc.html', context)


def login(request):
    context = {}
    if request.method == 'POST':
        context = {'welcome': True}

    return render(request, '../templates/login.html', context)


def additem(request):
    context = {}
    return render(request, '../templates/additem.html', context)


@require_GET
def updateitem(request):
    context = {'index': int(request.GET.get('index'))}
    return render(request, '../templates/updateitem.html', context)


def editAccount(request):
    context = {}
    return render(request, '../templates/editAccount.html', context)