from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login
from django.contrib import messages
import re
# Create your views here.
def is_valid_email(email):
      # Define the regex pattern for email validation
      pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
      return re.match(pattern, email)
  
def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if len(password)<8:
                messages.info(request, 'Password too short. Minimun 8 characters')
                return redirect('signup')
            if not re.findall('[A-Z]', password):
                messages.info(request, 'Password must contain at least one Cap')
                return redirect('signup')
            if not re.findall('[1-9]', password):
                messages.info(request, 'Password must contain at least one digit')
                return redirect('signup')
            if not is_valid_email(email):
                messages.info(request, 'email invalid')
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'Username Taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('accreated')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'core/signup.html')
    
def accreated(request):
    return render(request, 'core/accreated.html')

def connected(request):
    return render(request, 'core/connected.html')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['password']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            return redirect('connected')
        else:
            messages.error(request, "Wrong Information!!")
            return redirect('sigin')
    
    return render(request, "core/signin.html")