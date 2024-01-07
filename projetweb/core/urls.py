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
]
