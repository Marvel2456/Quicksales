from datetime import datetime
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser, LoggedIn

# Create your views here.

def loginUser(request):
    if request.method =='POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        

        
        if user is not None and user.is_subscribed==False:
            messages.info(request, f'Subscription has expired kindly renew to continue')
            return redirect('login')
        elif user is not None and user.is_subscribed==True:
            login(request, user)
            LoggedIn.objects.create(staff=user,
            login_id = datetime.now().timestamp(),
            timestamp = datetime.now()
            ).save()
            messages.success(request, f'Welcome {user.username}')
            return redirect('index')
        
        else:
            messages.info(request, 'Username or Password is not correct')

    return render(request, 'account/login.html')

def logoutUser(request):
    logout(request)
    # LoggedOut(staff = user,
    # logout_id = datetime.now().timestamp(),
    # ).save
    return redirect('login')
