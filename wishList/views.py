from django.shortcuts import render, redirect


def logout(request):
    if request.GET.get('logout', None):
        del request.session['loggedin']
        del request.session['loggedUsr']
    return redirect('/login')


def home(request):
    if 'loggedin' not in request.session:
        request.session['loggedin'] = None
    testUsr = ['danielRangel', 'christianSumares', 'justinLe', 'nayanGupta']
    testPass = "password"
    context = {}
    if request.session['loggedin'] == 1:
        return render(request, '../templates/home.html', context)

    usrField = request.POST.get('username', None)
    passField = request.POST.get('password', None)

    if (usrField is None) or (passField is None):
        return redirect('/login')

    if (usrField in testUsr) and (testPass == passField):
        request.session['loggedin'] = 1
        request.session['loggedUsr'] = usrField
        return render(request, '../templates/home.html', context)
    else:
        request.session['loggedin'] = 0
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
