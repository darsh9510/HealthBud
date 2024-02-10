from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('room/<str:pk>',views.room,name='room'),
    path('createroom',views.createRoom,name='createRoom'),
    path('delete/<str:pk>', views.deleteRoom, name='delete'),
    path('deletemsg/<str:pk>', views.deleteMessage, name='deletemsg'),
]