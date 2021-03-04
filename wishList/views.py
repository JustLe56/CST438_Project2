from django.shortcuts import render

def home(request):
    context = {}
    return render(request, 'home.html', context)

def create_account(request):
    context = {}
    return render(request, 'createAccount.html', context)