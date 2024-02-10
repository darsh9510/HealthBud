from django.shortcuts import render
from django.shortcuts import render,redirect
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages 
# Create your views here.
from .models import Rooms, Disease, Massage
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse
from .forms import RoomForm

def home(request):
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    room = Rooms.objects.filter(Q(name__icontains=q)|Q(disease__name__icontains=q))
    context = {'room':room,'count':room.count(),'q':q}
    return render(request, 'home.html', context)

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

def deleteRoom(request, pk):
    room = Rooms.objects.get(id=pk)
    if request.method == 'POST':
        if request.user != room.host:
            return HttpResponse('You are not allowed here')
        room.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj':room})

def deleteMessage(request, pk):
    message = Massage.objects.get(id=pk)
    room = Rooms.objects.get(id=message.room.id)
    if request.method == 'POST':
        if request.user != message.user:
            return HttpResponse('You are not allowed here')
        message.delete()
        return redirect('room',pk = room.id)
    return render(request, 'delete.html', {'obj':message})

