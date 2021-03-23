from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth import logout


def logout_usr(request):
    logout(request)
    return HttpResponseRedirect('/login')


def home(request):
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
    return render(request, '../templates/updateitem.html', context)


def editAccount(request):
    context = {}
    return render(request, '../templates/editAccount.html', context)
