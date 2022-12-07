from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django import template
from django.contrib.auth import get_user_model


# Create your views here.
def home(request):
    return render(request, "authentication/index.html")

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        name1 = request.POST.get('name1')
        name2 = request.POST.get('name2')
        email = request.POST.get('email')
        pass1 = request.POST.get('pass1')
        pass2 = request.POST.get('pass2')
        gender = request.POST.get('gender')

        #test
        myuser = User.objects.create_user(username, email, pass1)
        #myuser = User(username=username,  pass1=pass1, email=email)
        myuser.first_name = name1
        myuser.last_name = name2
        myuser.username = username
        myuser.gender = gender
        myuser.save()
        #messages.success(request, "Your account has been successfully created")
        return redirect("signin")

    return render(request, "authentication/signup.html")

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']
        
        user = authenticate(username=username, password=pass1)
        usermore = User.objects.get(username=username)
        if user is not None:
            login(request, user)
            name1 = user.first_name
            return render(request, "authentication/index.html", {'usermore': usermore})

        else:
            messages.error(request, "Bad credentials")
            return redirect('home')



    return render(request,"authentication/signin.html")

def signout(request):
    logout(request)
    return redirect('home')
