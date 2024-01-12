from django.urls import path
from . import views


urlpatterns = [
    
    path('', views.index, name="index"),
    path('signup', views.signup, name="signup"),
    path('signin', views.signin, name="signin"),
    path('settings', views.settings, name="settings"),
    path('logout', views.logout, name='logout'),
  
    path('newroom', views.newroom, name='newroom'),
    path('room/<int:room_id>', views.room, name='room'),

    path('getMessages/<int:room_id>/', views.getMessages, name='getMessages'),
    path('adm/<int:iduser>/<int:roomid>', views.admin, name='admin'),
    path('ban/<int:iduser>/<int:roomid>', views.ban, name='ban'),
    path('mute/<int:iduser>/<int:roomid>', views.mute, name='mute'),
    path('deletemessage/<int:messageid>', views.deletemessage, name='deletemessage'),
    path('openandclose/<int:roomid>', views.openandclose, name='openandclose'),
]
