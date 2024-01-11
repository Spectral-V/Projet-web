from django.shortcuts import render, redirect, get_object_or_404
from django import http
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Profile,Message,Room, Permission
import re
from django.http import HttpResponse, JsonResponse



# Create your views here.
def is_valid_email(email):
      # Define the regex pattern for email validation
      pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
      return re.match(pattern, email)



def index(request):
    return render(request, 'core/index.html')



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
            #log user in and redirect to settings page
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
            #create a Profile object for the new user
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
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
            return redirect('newroom')
        else:
            messages.error(request, "Wrong Information!!")
            return redirect('signin')
    
    return render(request, "core/signin.html")


@login_required(login_url='signin')
def settings(request):
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'core/settings.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')


@login_required
def newroom(request):
    if request.method == 'POST' :
        if request.POST['form-type'] == 'croom':
            roomname = request.POST['roomname']
            room = Room.objects.create(name = roomname)
            perm=Permission.objects.create(level="owner",user=Profile.objects.get(user=request.user),room=room,)
            perm.save
            room.save
            return http.HttpResponseRedirect('/room/%i'%room.room_id)
        if request.POST['form-type'] == "jroom":
            roomid = request.POST['roomid']
            a = int('0' + roomid)
            user=Profile.objects.get(user=request.user)
            
            if Room.objects.filter(room_id=a).exists():
                roomtojoin=Room.objects.get(room_id=a)
                if not Permission.objects.filter(user=user,room=roomtojoin).exists():
                
            
                    perm=Permission.objects.create(level="normal",user=Profile.objects.get(user=request.user),room=roomtojoin,)
                    perm.save
                    
                permi=Permission.objects.get(user=user,room=roomtojoin)
                if permi.level=="ban":
                    messages.info(request, 'Too bad, you are ban from this room')
                    return redirect('newroom')
                return http.HttpResponseRedirect('/room/%i'%a)
            messages.info(request, 'oh no this room does not exist, you should create it')
            return redirect('newroom')
            
        
    return render(request, 'core/newroom.html')

def joinroom(a,user,request):
            
            roomtojoin=Room.objects.get(room_id=a)
            if Room.objects.filter(room_id=a).exists():

                if not Permission.objects.filter(user=user,room=roomtojoin).exists():
                
            
                    perm=Permission.objects.create(level="normal",user=Profile.objects.get(user=request.user),room=roomtojoin,)
                    perm.save
                    return http.HttpResponseRedirect('/room/%i'%a)
                permi=Permission.objects.get(user=user,room=roomtojoin)
                if permi.level=="ban":
                    messages.info(request, 'Too bad, you are ban from this room')
                    return redirect('core/room.html')
                
            messages.info(request, 'oh no this room does not exist, you should create it')
            return redirect('core/newroom.html')

@login_required
def room(request,room_id):
    if request.method == 'POST' :
        if request.POST['form-type'] == "msg":
            mtext = request.POST['message']
            user_profile = Profile.objects.get(user=request.user)
            roomverif=Room.objects.get(room_id=room_id)
            perm=Permission.objects.get(user=user_profile,room=roomverif)
            if perm.level!="mute" and perm.level!="ban":


                m = Message(recipient=Room.objects.get(room_id=room_id), sender=user_profile,message=texttoemoji(mtext))
                m.save()

        if request.POST['form-type'] == "jroom":
            roomid = request.POST['roomid']
            a = int('0' + roomid)
            user=Profile.objects.get(user=request.user)
            
            if Room.objects.filter(room_id=a).exists():
                roomtojoin=Room.objects.get(room_id=a)
                if not Permission.objects.filter(user=user,room=roomtojoin).exists():
                
            
                    perm=Permission.objects.create(level="normal",user=Profile.objects.get(user=request.user),room=roomtojoin,)
                    perm.save
                    
                permi=Permission.objects.get(user=user,room=roomtojoin)
                if permi.level=="ban":
                    messages.info(request, 'Too bad, you are ban from this room')
                    return redirect('/room/%i'%room_id)
                return http.HttpResponseRedirect('/room/%i'%a)
            messages.info(request, 'oh no this room does not exist, you should create it')
            return redirect('/room/%i'%room_id)
     
    u =  Profile.objects.get(user=request.user)
    context = {
            'room': Room.objects.get(room_id=room_id),
            'mess': Message.objects.filter(recipient_id=room_id),
            'user': u,
            'perm': Permission.objects.get(user=u, room=room_id)}
    
    return render(request, 'core/room.html', context)


@login_required
def getMessages(request, room_id):
    room_details = Room.objects.get(room_id=room_id)
    if request.method == 'GET':
        mess = Message.objects.filter(recipient=room_details)
        list = []
        for m in mess:
            list.append({
                'sender': m.sender.user.username,
                'message': m.message,
                'date': m.date.strftime("%d/%m/%Y %H:%M:%S"),
                
            })
    
    return JsonResponse({"mess":list})


    
def texttoemoji(text):
    smileystoemojis = {
        ":)": "😊",
        ":(": "☹️",
        ":O": "😮",
        ":D": "😀",
        ":P": "😛",
        ":|": "😐",
        ":/": "😕",
        ";)": "😉",
        "<3": "❤️",
        "[pasteque]": "🍉",
    }
    for smiley, emoji in smileystoemojis.items():
        text = re.sub(re.escape(smiley), emoji, text)

    return text

@login_required
def admin(request,iduser,roomid ):
    upuser=Profile.objects.get(id_user=iduser)
    uproom=Room.objects.get(room_id=roomid)
    perm=Permission.objects.get(user=upuser,room=uproom)
    perm.level="admin"
    perm.save

@login_required
def ban(request,iduser,roomid ):
    upuser=Profile.objects.get(id_user=iduser)

    uproom=Room.objects.get(room_id=roomid)
    perm=Permission.objects.get(user=upuser,room=uproom)
    if perm!="owner":
        perm.level="ban"
        perm.save

@login_required
def mute(request,iduser,roomid ):
    upuser=Profile.objects.get(id_user=iduser)
    uproom=Room.objects.get(room_id=roomid)
    perm=Permission.objects.get(user=upuser,room=uproom)
    if perm!="owner":
        perm.level="mute"
        perm.save



