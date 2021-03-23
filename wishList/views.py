from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.http import require_POST
import json

@require_POST
def add_item(request):
    data = json.loads(request.body)
    rm = int(data.get('rm', None))
    if rm == -1:
        new_item = {
            "name": data.get('name', None),
            "url": data.get('url', None),
            "img_url": data.get('img_url', None),
            "description": data.get('description', None),
            "priority": int(data.get('priority', None))
        }
        request.session['items'].append(new_item)
        msg = 'item added'
    else:
        request.session['items'].pop(rm)
        msg = 'item deleted'

    request.session['items'] = (sorted(request.session['items'], key=lambda i: (i['priority'], i['name'])))
    return JsonResponse({'detail': msg})


def logout_usr(request):
    logout(request)
    return HttpResponseRedirect('/login')


def home(request):
    if 'items' not in request.session:
        test_item = {
            "name": "wallet",
            "url": "google.com",
            "img_url": "google.com",
            "description": "cool wallet",
            "priority": 1
        }
        request.session['items'] = list()
        request.session['items'].append(test_item)
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

def updateitem(request):
    context = {}
    return render(request, '../templates/updateItem.html', context)

def editAccount(request):
    context = {}
    return render(request, '../templates/editAccount.html', context)


def refresh_list(request):
    return render(request, '../templates/list.html')