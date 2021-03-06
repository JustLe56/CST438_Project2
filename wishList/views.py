from django.shortcuts import render

def home(request):
    context = {}
    return render(request, '../templates/home.html', context)
def createAcc(request):
    context = {}
    return render(request, '../templates/createAcc.html', context)