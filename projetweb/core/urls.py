from django.urls import path
from . import views

urlpatterns = [
    path('signup', views.signup, name="signup"),
    path('accreated', views.accreated, name="accreated")
]
