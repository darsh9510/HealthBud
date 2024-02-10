from django.shortcuts import render
from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages 
# Create your views here.
from .models import Rooms, Disease, Massage,Doctor
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import RoomForm
import requests

# Define the base URL
URL = "https://ap-south-1.aws.neurelo.com/"
base_url = URL + "custom/auth"

# Set the query parameters
query_params = {
    "doctor_name": "",
    "registration_no": "",
    "registration_year": "",
    "state_medical_council": "\\"
}

# Define the headers
headers = {
    "X-API-KEY": "neurelo_9wKFBp874Z5xFw6ZCfvhXUBh9Hd4NW9ZwiLJ7tCsik3n3sDPi8tNL1xbmK4rsM539IXn6dRbBr6dZ8rJuWLIQLUP4vx349mJYHvEB4FCBAoD7WIvBt6MkzUEB/cbpfJkS2OypqIq9h3yaMIeJPTr5eSA4/eGjFoLJtkBt2gtyG22h96Fgg/Kil97x4vyvXqH_x9Ond+P7bK85/+ElhF4/vc9pzj18mx9aPM9/32SuEUc="
}

# Make the GET request
def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room = Rooms.objects.filter(Q(name__icontains=q)|Q(disease__name__icontains=q))
    context = {'room':room,'count':room.count(),'q':q}
    return render(request, 'home.html', context)

def signin_as_d(request):
    if request.method == 'POST':
        doctor_name = request.POST['doctor_name']
        registration_no = request.POST['registration_no']
        registration_year = request.POST['registration_year']
        state_medical_council = request.POST['state_medical_council']
        password = request.POST['password']
        disease_m = request.POST['disease']

        u_exist = User.objects.filter(username=doctor_name).exists()
        if u_exist:
            messages.info(request, 'User already exists')
            return redirect('sign_as_doctor')



        query_params["doctor_name"] = doctor_name
        query_params["registration_no"] = registration_no
        query_params["registration_year"] = registration_year
        query_params["state_medical_council"] = state_medical_council
        
        response = requests.get(base_url, params=query_params, headers=headers)

    # Check if the request was successful (status code 200)
        if response.status_code == 200:
            # Print the response content
            exists = Disease.objects.filter(name=disease_m).exists()
            if exists:
                disease_m_obj = Disease.objects.get(name=disease_m)
            else:
                disease_m_obj = Disease.objects.create(name=disease_m)
            user = User.objects.create_user(doctor_name, password=password)
            user.save()
            doctor = Doctor.objects.create(doctor = user,registration_no= registration_no,registration_year = registration_year,state_medical_council = state_medical_council,disease = disease_m_obj)
            print(response.text)
        else:
            # Print an error message
            print("Error:", response.status_code)
        return redirect('signin')
    return render(request, 'signin_as_d.html')


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
    return render(request,'signin.html',context)

def signup(request):
    page = 'signup'
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('signin.html')
    else:
        form = UserCreationForm()

    return render(request, 'signin.html', {'form': form})



def room(request, pk):
    room = Rooms.objects.get(id=pk)
    user = User.objects.all()
    messages = Massage.objects.filter(room=room)
    context = {'room': room, 'messages': messages,'a_user':user}

    if request.method == 'POST':
        if 'participant_username' in request.POST:
            participant_username = request.POST.get('participant_username')
            try:
                participant = User.objects.get(username=participant_username)
                room.participent.add(participant)
            except User.DoesNotExist:
                pass
        else:
            message_text = request.POST.get('message')
            message = Massage.objects.create(user=request.user, room=room, text=message_text)
            return redirect('room', pk=room.id)

    return render(request, 'room.html', context)


@login_required(login_url='signin')
def createRoom(request):
    form = RoomForm()
    if request.method == 'POST':
        room_name = request.POST.get('room_name')
        host_user = request.user
        disease_id = request.POST.get('disease')
        disease_obj = Disease.objects.get(name=disease_id)
        disease_id = disease_obj.id
        room = Rooms.objects.create(
            name=room_name,
            host=host_user,
            disease_id=disease_id,
        )
        room.participent.add(host_user)
        return redirect('home')
    context = {'form':form}
    return render(request, 'c_room.html',context)


@login_required(login_url='signin')
def deleteRoom(request, pk):
    room = Rooms.objects.get(id=pk)
    if request.method == 'POST':
        if request.user != room.host:
            return HttpResponse('You are not allowed here')
        room.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj':room})

@login_required(login_url='signin')
def deleteMessage(request, pk):
    message = Massage.objects.get(id=pk)
    room = Rooms.objects.get(id=message.room.id)
    if request.method == 'POST':
        if request.user != message.user:
            return HttpResponse('You are not allowed here')
        message.delete()
        return redirect('room',pk = room.id)
    return render(request, 'delete.html', {'obj':message})

@login_required(login_url='signin')
def resetpasswd(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        users = User.objects.get(username=username)
        if users.id is not request.user.id:
            return HttpResponse('You are not allowed here')
        users.set_password(password)
        users.save()
        return redirect('signin')
    context = {}
    return render(request, 'resetpasswd.html')
    return render(request, 'resetpasswd.html')

@login_required(login_url='signin')
def logout_u(request):
    logout(request)
    return redirect('home')