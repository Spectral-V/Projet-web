from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('accreated', views.accreated, name="accreated"),
    path('signin', views.signin, name="signin"),
    path('connected', views.connected, name="connected"),
    path('settings', views.settings, name="settings"),
    path('logout', views.logout, name='logout'),
  
    path('newroom', views.newroom, name='newroom'),
    path('room/<int:room_id>', views.room, name='room'),

    path('getMessages/<int:room_id>/', views.getMessages, name='getMessages'),
    path('roomadmin', views.admin, name='admin'),
    path('ban', views.ban, name='ban'),
    path('mute', views.mute, name='mute'),
    path('deletemessage/<int:messageid>', views.deletemessage, name='deletemessage'),
]
