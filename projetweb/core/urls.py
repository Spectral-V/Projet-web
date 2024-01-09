from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('chat',views.chat,name='chat'),
    path('accreated', views.accreated, name="accreated"),
    path('signin', views.signin, name="signin"),
    path('connected', views.connected, name="connected"),
    path('settings', views.settings, name="settings"),
    path('logout', views.logout, name='logout'),
    path('search-users/', views.search_users, name='search_users'),
    path('messaging/int:user_id/', views.messaging, name='messaging'),
    path('send-message/int:user_id/', views.send_message, name='send_message'),
    path('newroom', views.newroom, name='newroom'),
    path('room/<int:room_id>', views.room, name='room'),
]
