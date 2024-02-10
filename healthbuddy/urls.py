from django.urls import path
from . import views
urlpatterns = [
    path('',views.home,name='home'),
    path('signup/',views.signup,name='signup'),
    path('signin/',views.signin,name='signin'),
    path('room/<str:pk>',views.room,name='room'),
    path('question/',views.quest,name='question'),
    path('createroom',views.createRoom,name='createRoom'),
    path('delete/<str:pk>', views.deleteRoom, name='delete'),
    path('deletemsg/<str:pk>', views.deleteMessage, name='deletemsg'),
    path('logout', views.logout_u, name='logout'),
    path('resetpasswd', views.resetpasswd, name='resetpasswd'),
    path('sign_as_doctor',views.signin_as_d,name='sign_as_doctor'),
    path('recommendation', views.recom, name='recommendation'),
]
