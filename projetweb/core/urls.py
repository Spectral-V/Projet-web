from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name="signup"),
    path('accreated', views.accreated, name="accreated"),
    path('signin', views.signin, name="signin"),
    path('connected', views.connected, name="connected")
]
