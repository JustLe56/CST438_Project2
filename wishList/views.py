from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json

@csrf_exempt
@require_POST
def load_items(request):
    data = json.loads(request.body)
    request.session['items'] = (sorted(data, key=lambda i: (i['priority'], i['name'])))
    return JsonResponse({'detail': "items_loaded"})


# @csrf_exempt
# @require_POST
# def add_item(request):
#     decode_data = request.body.decode('utf-8')
#     data = json.loads(decode_data)
#
#     rm = data.get('rm', None)
#     if rm is None:
#         data['index'] = len(request.session['items'])
#         request.session['items'].append(data)
#         msg = 'item added'
#     else:
#         rm = int(rm)
#         msg = request.session['items'][rm]
#         msg = msg['index']
#         request.session['items'].pop(rm)
#
#     request.session['items'] = (sorted(request.session['items'], key=lambda i: (i['priority'], i['name'])))
#     return JsonResponse({'detail': msg})


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
    global wishlist
    context = {'items': wishlist}
    return render(request, '../templates/additem.html', context)


def updateitem(request):
    context = {}
    return render(request, '../templates/updateitem.html', context)


def editAccount(request):
    context = {}
    return render(request, '../templates/editAccount.html', context)


def refresh_list(request):
    return render(request, '../templates/list.html')
