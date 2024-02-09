from django.shortcuts import render
from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages 
# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from django.contrib.auth import get_user_model

User = get_user_model()

def home(request):
    return render(request,'home.html')

def signin(request):
    page = 'signin'
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            messages.info(request,'invalid credentials')
            return redirect('signin')
    context = {'page': page}
    return render(request,'base/signin.html',context)

def signup(request):
    page = 'signup'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('base/signin.html')
    else:
        form = UserCreationForm()

    return render(request, 'base/signin.html', {'form': form})
 