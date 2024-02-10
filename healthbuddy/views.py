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
import dill
import numpy as np
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
    room_u = Rooms.objects.filter(host=request.user.id)
    context = {'room':room,'count':room.count(),'q':q,'room_u':room_u}

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
    room_u = Rooms.objects.filter(host=request.user.id)
    messages = Massage.objects.filter(room=room)
    context = {'room': room, 'messages': messages,'a_user':user,'room_u':room_u}

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

ques = [
        [1, 'itching'],
    [2, 'skin_rash'],
    [3, 'continuous_sneezing'],
    [4, 'shivering'],
    [5, 'chills'],
    [6, 'joint_pain'],
    [7, 'stomach_pain'],
    [8, 'acidity'],
    [9, 'vomiting'],
    [10, 'burning_micturition'],
    [11, 'fatigue'],
    [12, 'cold_hands_and_feets'],
    [13, 'mood_swings'],
    [14, 'weight_loss'],
    [15, 'restlessness'],
    [16, 'lethargy'],
    [17, 'cough'],
    [18, 'high_fever'],
    [19, 'sunken_eyes'],
    [20, 'breathlessness'],
    [21, 'sweating'],
    [22, 'indigestion'],
    [23, 'headache'],
    [24, 'yellowish_skin'],
    [25, 'dark_urine'],
    [26, 'nausea'],
    [27, 'loss_of_appetite'],
    [28, 'back_pain'],
    [29, 'constipation'],
    [30, 'abdominal_pain'],
    [31, 'diarrhoea'],
    [32, 'mild_fever'],
    [33, 'yellowing_of_eyes'],
    [34, 'acute_liver_failure'],
    [35, 'swelled_lymph_nodes'],
    [36, 'malaise'],
    [37, 'blurred_and_distorted_vision'],
    [38, 'phlegm'],
    [39, 'throat_irritation'],
    [40, 'redness_of_eyes'],
    [41, 'sinus_pressure'],
    [42, 'chest_pain'],
    [43, 'fast_heart_rate'],
    [44, 'pain_during_bowel_movements'],
    [45, 'neck_pain'],
    [46, 'dizziness'],
    [47, 'obesity'],
    [48, 'puffy_face_and_eyes'],
    [49, 'enlarged_thyroid'],
    [50, 'swollen_extremities'],
    [51, 'excessive_hunger'],
    [52, 'drying_and_tingling_lips'],
    [53, 'slurred_speech'],
    [54, 'muscle_weakness'],
    [55, 'stiff_neck'],
    [56, 'swelling_joints'],
    [57, 'loss_of_balance'],
    [58, 'loss_of_smell'],
    [59, 'foul_smell_of_urine'],
    [60, 'passage_of_gases'],
    [61, 'internal_itching'],
    [62, 'toxic_look_(typhos)'],
    [63, 'depression'],
    [64, 'irritability'],
    [65, 'muscle_pain'],
    [66, 'red_spots_over_body'],
    [67, 'abnormal_menstruation'],
    [68, 'watering_from_eyes'],
    [69, 'increased_appetite'],
    [70, 'family_history'],
    [71, 'visual_disturbances'],
    [72, 'receiving_blood_transfusion'],
    [73, 'receiving_unsterile_injections'],
    [74, 'stomach_bleeding'],
    [75, 'history_of_alcohol_consumption'],
    [76, 'blood_in_sputum'],
    [77, 'palpitations'],
    [78, 'painful_walking'],
    [79, 'scurring'],
    [80, 'blister'],
]
ds=['Fungal infection', 'Allergy', 'GERD', 'Chronic cholestasis', 'Drug Reaction', 'Peptic ulcer disease', 'AIDS', 'Diabetes', 'Gastroenteritis', 'Bronchial Asthma', 'Hypertension', 'Migraine', 'Cervical spondylosis', 'Paralysis (brain hemorrhage)', 'Jaundice', 'Malaria', 'Chicken pox', 'Dengue', 'Typhoid', 'Hepatitis A', 'Hepatitis B', 'Hepatitis C', 'Hepatitis D', 'Hepatitis E', 'Alcoholic hepatitis', 'Tuberculosis', 'Common Cold', 'Pneumonia', 'Dimorphic hemorrhoids (piles)', 'Heart attack', 'Varicose veins', 'Hypothyroidism', 'Hyperthyroidism', 'Hypoglycemia', 'Osteoarthritis', 'Arthritis', '(vertigo) Paroxysmal Positional Vertigo', 'Acne', 'Urinary tract infection', 'Psoriasis', 'Impetigo']

global_probs = [None]
global_tops=[None]
#print(ques[::][0])
Response = []
def quest(request):
    global global_probs
    global global_tops
    def predictions():
        res=np.asarray(Response).reshape(1,80)
        print(res)
        with open('//home/phinex/Desktop/HealthBud/healthbuddy/mlh.pkl','rb') as f:
            pipe=dill.load(f)
        y_pred=pipe.predict(res)
        print(y_pred)
        top_labels=np.argsort(y_pred,axis=1)[:,-4:]
        probs=np.sort(y_pred,axis=1)[:,-4:]
        return top_labels,probs
    
    context = {'ques':ques}
    if(request.method == 'POST'):

        data = request.POST
        for i in ques:
            temp = data.get(str(i[0]))
            if temp == 'True':
                Response.append(True)
            else:
                Response.append(False)
        top_label ,probs= predictions()
        list_new = list(top_label.flatten())
        print(probs)
        print(list_new)
        top=[]
        for i in list_new:
            top.append(ds[i])
        print(top)
        global_probs=probs
        global_tops=top_label
        return redirect('recommendation')
    return render(request, 'question.html',context)

def recom(request):
    context = {'probs':global_probs,'tops':global_tops}
    return render(request, 'recommendation.html',context)
