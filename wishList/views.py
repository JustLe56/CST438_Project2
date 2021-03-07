from django.shortcuts import render, redirect


def logout(request):
    if request.GET.get('logout', None):
        del request.session['loggedin']
        request.session['loggedin'] = 0
    return redirect('createAcc')


def home(request):
    if 'loggedin' not in request.session:
        request.session['loggedin'] = 0
    testUsr = ['danielRangel', 'christianSumares', 'justinLe', 'nayanGupta']
    testPass = "password"
    context = {}
    if request.session['loggedin'] == 1:
        return render(request, '../templates/home.html', context)

    usrField = request.POST.get('username', None)
    passField = request.POST.get('password', None)

    if (usrField in testUsr) and (testPass == passField):
        request.session['loggedin'] = 1
        request.session['loggedUsr'] = usrField
        return render(request, '../templates/home.html', context)
    else:
        request.session['loggedin'] = 0
        return redirect('createAccount/')




def createAcc(request):
    context = {}
    if request.session['loggedin'] == 0:
        return render(request, '../templates/createAcc.html', context)
    else:
        return redirect('')
