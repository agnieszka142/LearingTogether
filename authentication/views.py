from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django import template


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



        #test
        myuser = User.objects.create_user(username, email, pass1)
        #myuser = User(username=username,  pass1=pass1, email=email)
        myuser.name1 = name1
        myuser.name2 = name2
        myuser.username = username
        myuser.save()
        messages.success(request, "Your account has been successfully created")

        return redirect("signin")

    return render(request, "authentication/signup.html")

def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        pass1 = request.POST['pass1']

        user = authenticate(username=username, password=pass1)

        if user is not None:
            login(request, user)
            name1 = user.first_name
            return render(request, "authentication/index.html", {'name1': name1})

        else:
            messages.error(request, "Bad credentials")
            return redirect('home')



    return render(request,"authentication/signin.html")

def signout(request):
    pass
