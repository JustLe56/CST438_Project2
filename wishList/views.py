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
    if 'loggedUsr' not in request.session:
        return render(request, '../templates/login.html', context)
    else:
        return redirect('')

def additem(request):
    context = {}
    return render (request,'../templates/additem.html',context)

def editAccount(request):
    context = {}
    return render (request,'../templates/editAccount.html',context)