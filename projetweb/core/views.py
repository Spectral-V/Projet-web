from django.shortcuts import render, redirect, get_object_or_404
from django import http
from django.contrib.auth.models import User, auth
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages as aler
from .models import Profile,Message,Room, Permission
import re
from django.http import HttpResponse, JsonResponse



def is_valid_email(email):
      # check if the mail has @ and .
      pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
      return re.match(pattern, email)



def index(request):
    return render(request, 'core/index.html')



def signup(request):
    #create an account
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']
        # get the different post from signup.html

        if password == password2:
            if len(password)<8:
                aler.info(request, 'Password too short. Minimun 8 characters')
                return redirect('signup')
            if not re.findall('[A-Z]', password):
                aler.info(request, 'Password must contain at least one Cap')
                return redirect('signup')
            if not re.findall('[1-9]', password):
                aler.info(request, 'Password must contain at least one digit')
                return redirect('signup')
            if not is_valid_email(email):
                aler.info(request, 'email invalid')
                return redirect('signup')
            if User.objects.filter(email=email).exists():
                aler.info(request, 'Email Taken')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                aler.info(request, 'Username Taken')
                return redirect('signup')

            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
            #create a user
                user_login = auth.authenticate(username=username, password=password)
                auth.login(request, user_login)
            #create a Profile 
                user_model = User.objects.get(username=username)
                new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            aler.info(request, 'Password Not Matching')
            return redirect('signup')
    else:
        return render(request, 'core/signup.html',{'alers': aler.get_messages(request)})
    

def signin(request):
    #to register
    if request.method == 'POST':
        username = request.POST['username']
        pass1 = request.POST['password']
        
        user = authenticate(username=username, password=pass1)
        
        if user is not None:
            login(request, user)
            return redirect('newroom')
        else:
            aler.error(request, "Wrong Information!!")
            return redirect('signin')
    
    return render(request, "core/signin.html",{'alers': aler.get_messages(request)})


@login_required(login_url='signin')
def settings(request):
    #allow you to put a profile picture (and to change your bio even if it s useless)
    user_profile = Profile.objects.get(user=request.user)

    if request.method == 'POST':
        if request.POST['form-type'] == 'cc':
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
        if request.POST['form-type'] == 'jr':
            return redirect('newroom')
    return render(request, 'core/settings.html', {'user_profile': user_profile})

@login_required(login_url='signin')
def logout(request):
    #disconect the user and send him on signin
    auth.logout(request)
    return redirect('signin')


@login_required
def newroom(request):
    #all the thing we can do in newroom
    if request.method == 'POST' :
        if request.POST['form-type'] == 'croom':
             #create a room and give the creator the owner permission
            roomname = request.POST['roomname']
            room = Room.objects.create(name = roomname)
            perm=Permission.objects.create(level="owner",user=Profile.objects.get(user=request.user),room=room,)
            perm.save
            room.save
            return http.HttpResponseRedirect('/room/%i'%room.room_id)
        if request.POST['form-type'] == "jroom":
            #join a room if the user can and if the room exists
            roomid = request.POST['roomid']
            a = int('0' + roomid)
            user=Profile.objects.get(user=request.user)
            
            if Room.objects.filter(room_id=a).exists():
                roomtojoin=Room.objects.get(room_id=a)
                if (not Permission.objects.filter(user=user,room=roomtojoin).exists()) and roomtojoin.open == "yes":
                
            
                    perm=Permission.objects.create(level="normal",user=Profile.objects.get(user=request.user),room=roomtojoin,)
                    perm.save
                if Permission.objects.filter(user=user,room=roomtojoin).exists():
                    permi=Permission.objects.get(user=user,room=roomtojoin)
                    if permi.level=="ban":
                        aler.info(request, 'Too bad, you are ban from this room')
                        return redirect('newroom')
                    return http.HttpResponseRedirect('/room/%i'%a)
                aler.info(request, 'room closed, and you re not in womp womp...')
                return redirect('newroom')
            aler.info(request, 'oh no this room does not exist, you should create it')
            return redirect('newroom')
            
        
    return render(request, 'core/newroom.html',{'alers': aler.get_messages(request)})



@login_required
def room(request,room_id):
    #all the thing we can do in newroom
    room=Room.objects.get(room_id=room_id)
    if request.method == 'POST' :
        if request.POST['form-type'] == "msg":
            #send a message
            mtext = request.POST['message']
            user_profile = Profile.objects.get(user=request.user)
            roomverif=Room.objects.get(room_id=room_id)
            perm=Permission.objects.get(user=user_profile,room=roomverif)
            if perm.level!="mute" and perm.level!="ban":


                m = Message(recipient=Room.objects.get(room_id=room_id), sender=user_profile,message=texttoemoji(mtext))
                m.save()
        if request.POST['form-type'] == "logout":
            #to disconect
            return redirect('logout')
        if request.POST['form-type'] == "jroom":
            #join a room if the user can and if the room exists
            roomid = request.POST['roomid']
            a = int('0' + roomid)
            user=Profile.objects.get(user=request.user)
            
            if Room.objects.filter(room_id=a).exists():
                roomtojoin=Room.objects.get(room_id=a)
                if (not Permission.objects.filter(user=user,room=roomtojoin).exists()) and roomtojoin.open == "yes":
                
            
                    perm=Permission.objects.create(level="normal",user=Profile.objects.get(user=request.user),room=roomtojoin,)
                    perm.save
                if Permission.objects.filter(user=user,room=roomtojoin).exists():
                    permi=Permission.objects.get(user=user,room=roomtojoin)
                    if permi.level=="ban":
                        aler.info(request, 'Too bad, you are ban from this room')
                        return redirect('/room/%i'%room.room_id)
                    return http.HttpResponseRedirect('/room/%i'%a)
                aler.info(request, 'room closed, and you re not in womp womp...')
                return redirect('/room/%i'%room.room_id)
            aler.info(request, 'oh no this room does not exist, you should create it')
            return redirect('/room/%i'%room.room_id)
        if request.POST['form-type'] == "croom":
            #create a room and give the creator the owner permission
            roomname = request.POST['roomname']
            room = Room.objects.create(name = roomname)
            perm=Permission.objects.create(level="owner",user=Profile.objects.get(user=request.user),room=room,)
            perm.save
            room.save
            return http.HttpResponseRedirect('/room/%i'%room.room_id)
     
    u =  Profile.objects.get(user=request.user)
    context = {
        #all the info room needs
            'room': Room.objects.get(room_id=room_id),
            'mess': Message.objects.filter(recipient_id=room_id),
            'user': u,
            'perm': Permission.objects.get(user=u, room=room_id),
            'permr': Permission.objects.filter(room=room_id),
            'alers': aler.get_messages(request),
            }
    
    return render(request, 'core/room.html', context)


@login_required
def getMessages(request, room_id):
    #get all the messages from a room and send them
    upuser=Profile.objects.get(user=request.user)
    room_details = Room.objects.get(room_id=room_id)
    perm=Permission.objects.get(user=upuser,room=room_details)
    if perm.level!="ban":
        
            if request.method == 'GET':
                mess = Message.objects.filter(recipient=room_details)
                list = []
            for m in mess:
                list.append({
                    'senderid': m.sender.id_user,
                    'sender': m.sender.user.username,
                    'message': m.message,
                    'date': m.date.strftime("%d/%m/%Y %H:%M:%S"),
                    'id': m.message_id,
                    'roomid': room_id,
                
                 })
    
            return JsonResponse({"mess":list})
    return http.JsonResponse({'status': 'ok'})


    
def texttoemoji(text):
    #change all the emoji and some protection against html injection
    smileystoemojis = {
        ":)": "😊",
        ":(": "☹️",
        ":O": "😮",
        ":D": "😀",
        ":P": "😛",
        ":|": "😐",
        ";)": "😉",
        "<3": "❤️",
        "[pasteque]": "🍉",
        "<": "&lsaquo;",
        ">": "&rsaquo;",
        "[discard]": "<a href='http://www.alban.alwaysdata.net/discard/'>discard.com</a>"
    }
    for smiley, emoji in smileystoemojis.items():
        text = re.sub(re.escape(smiley), emoji, text)

    return text

@login_required
def admin(request,iduser,roomid ):
    #change the permission to admin
    
    upuser=Profile.objects.get(id_user=iduser)
    uproom=Room.objects.get(room_id=roomid)
    perm=Permission.objects.get(user=upuser,room=uproom)
    if perm.level!="owner":
        if perm.level!="admin":
            perm.level="admin"
            perm.save()
            return http.JsonResponse({'status': 'admin'})
        elif perm.level=="admin":
            perm.level="normal"
            perm.save()
            return http.JsonResponse({'status': 'unadmin'})


@login_required
def ban(request,iduser,roomid ):
    #change the permission to ban
    upuser=Profile.objects.get(id_user=iduser)
    uproom=Room.objects.get(room_id=roomid)
    perm=Permission.objects.get(user=upuser,room=uproom)
    if perm.level!="owner":
        if perm.level == "ban" :
            perm.level="normal"
            perm.save()
            return http.JsonResponse({'status': 'unban'})
        elif perm.level!="ban":
            perm.level="ban"
            perm.save()
            return http.JsonResponse({'status': 'ban'})

@login_required
def mute(request,iduser,roomid ):
    #change the permission to mute
    upuser=Profile.objects.get(id_user=iduser)
    uproom=Room.objects.get(room_id=roomid)
    perm=Permission.objects.get(user=upuser,room=uproom)
    if perm.level!="owner":
        if perm.level!="mute":
            perm.level="mute"
            perm.save()
            return http.JsonResponse({'status': 'mute'})
        else:
            perm.level="normal"
            perm.save()
            return http.JsonResponse({'status': 'unmute'})

@login_required
def deletemessage(request, messageid):
    if request.method == 'GET' :
        mess = Message.objects.get(message_id=messageid)
        mess.delete()
    
    return http.JsonResponse({'status': 'ok'})

@login_required
def openandclose(request, roomid):
    #close or open a room
    if request.method == 'GET' :
        uproom=Room.objects.get(room_id=roomid)
        n="no"
        y="yes"
        if uproom.open == y:
                uproom.open = n
                uproom.save()
        elif uproom.open == n:
                uproom.open = y 
                uproom.save()

        
    
    return http.JsonResponse({'status': 'ok'})
    




