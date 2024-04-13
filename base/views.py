from django.shortcuts import render , redirect
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required #meka awilla users lata ha onema kenukt pages access restrict krnna one krna import ekk, meken thami e restrict kirima sidda krnne
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Rooms , Topic, Message
from .forms import RoomForm

# Create your views here.

# rooms = [
#        {'id' : 1 , 'name': 'lets learn python'},
#        {'id' : 2 , 'name': 'desitgn with me'},
#        {'id' : 3 , 'name': 'frontend developers'},

# ]


#creating a view for the login page

def loginPage(request): #mekt login nama yodagnne natte hdpu functions ekk thiynwa login eka naming conflicts enna puluwan hinda eka danne natte e nama

       page = 'login'

       if request.user.is_authenticated:
              return redirect('home') # me if statment ekn wenne user alreacy loged in nm aaye boruwat login page ekt yna eka therumak nhane, wardila hari login page ekt yanna unoth aphu redirect krnwanwa home page ekt
       

       if request.method == 'POST':
              username = request.POST.get('username').lower()
              password =request.POST.get('password') #me username saha password deka enne frontned ekn dena username password deki dan pai meka database eke user credntial ekk samana krnna one

              try:
                     user = User.objects.get(username = username) #check kala user exists da kiyla
              except:
                     messages.error(request, 'User does not exsit..') #nattnm flash messgaes walin messga ekak front ed ekat dunna

              user = authenticate(request, username = username, password = password) #user wa autheniticate krgtta

              if user is not None: #user innwa nm user wa autheticate una nm
                     login(request, user) #login wenwa
                     return redirect('home')

              else:
                     messages.error(request, "username or password does not exsist")
       context = {'page' : page}
       return render(request, 'base/login_register.html' , context)


def logoutUser(request):
       logout(request)
       return redirect('home')

def registerPage(request):
       form = UserCreationForm()
       print(request.POST)

       if request.method ==  "POST":
              form =  UserCreationForm(request.POST)
              if form.is_valid():
                     user = form.save(commit = False) #meke theruma awilla user wa hduwain passe e hdna user object eka code ekn meline ekan passe access krnna one widiyt hdgnnwa kiyna ek

                     user.username = user.username.lower()
                     user.save()

                     login(request, user); # me code line eka  saha eta pahala code line ekn karnne user register unain passe kelin registered user login user knk widiyt home pafge ekt redirect krnwa
                     return redirect('home')
              
              else:
                     messages.error(request, "Something went wrong!!")


       return render(request, 'base/login_register.html', {'form' : form} )


def home(request):
        q = request.GET.get('q') if request.GET.get('q') != None else ''
        rooms = Rooms.objects.filter(Q(topic__name__icontains=q) | 
                                     Q(name__icontains=q) | 
                                     Q(description__icontains=q)) #Rooms.objects.all()meken rooms  table ekt jhdpu okkoma record rooms kiyna variable eke save wenwa
       #methan me topic_name_icntains kiynne q query ekt adlwa thiyna text eka onema topic ekak thiynwa nm eka room variable ekt ganna kiyla, methna iconatins arunama startswith ends with wage ewath denna pulwuan

        topics = Topic.objects.all()
        room_count = rooms.count()
        room_messages = Message.objects.filter(Q(room__topic__name__icontains = q))

        return render(request, 'base/home.html' , {'rooms': rooms, 'topics' : topics , 'room_count': room_count , 'room_messages' : room_messages}) 

def room(request,pk): #methan pk kiyl damma dynamic url routing widiyt url file eke denna puluwan <str:pk> widiyt (url file eka blnna)
       
#       room = None
#       for i in rooms:
#              if i['id'] == int(pk):
#                     room = i 


       room = Rooms.objects.get(id=pk)  
       room_messages = room.message_set.all() #.order_by('-created')/ # meke oredr by ekn krnne filter krna eka most recent messages ganna
       participants = room.participants.all() #many to many relationship ekk participants la athar ha room arthar hdla  eka room view method ekt genaawa mekn


       if request.method == "POST":
              message = Message.objects.create(
                     user = request.user,
                     room = room,
                     body = request.POST.get('messageBody')
              )
              room.participants.add(request.user)
              return redirect('room', pk = room.id)

       context = {'room': room , 'room_messages' : room_messages, 'participants' : participants}
       return render(request, 'base/room.html' , context)


def userProfile(request, pk):
       user = User.objects.get(id = pk)
       print(user)
       rooms = user.rooms_set.all() #from room_set, we can get all the childern of a specific object
       room_messages = user.message_set.all()
       topics = Topic.objects.all()

       context  = {'user' : user, 'rooms' : rooms , "room_messages" : room_messages , 'topics' : topics }
       return render (request, 'base/profile.html' , context)

@login_required(login_url='login') #meka decorator ekak
def createRoom(request):

       form = RoomForm()
       if request.method == 'POST':
              form = RoomForm(request.POST)
              if form.is_valid():
                     form.save()
                     return redirect("home")

       context = { 'form': form }
       return render(request, 'base/room_form.html', context)

@login_required(login_url='login') #meka decorator ekak
def updateRoom(request, pk):
       room = Rooms.objects.get(id=pk) #mekn krnne data base eke thiyna okkoma room athrin url eke thiyna id ekat adla rom eke wisthra tika aragnnwa
       form = RoomForm(instance=room) #mekn krnne update room page ekt giyma form ekk thiynawa, e form ekn thami apita update krnna one dewal api type krnne, namuth room id eka dunnain passe e form eka e room id ekat adlwa thiyna data walin prefill wela enwa menna me code line eka hinda , apita  thiynne eta passe apita one krna dewal walin eka fill krnna

       if request.user != room.host:
              return HttpResponse('You are not allowed here!!') #mkeat thami htp response eka import kale udadi, emehm http response ekk denwa django http ekn http response eka import krgnna one
       

       if request.method == 'POST':
              form = RoomForm(request.POST, instance=room) #meken kiynne request eke thiyna data walin insatance = room kiyla thiyna placeholders purawanna kiyna eka 
              if form.is_valid():
                     form.save()
                     return redirect('home')

       context = {'form' : form} 
       return render (request, "base/room_form.html" , context)


@login_required(login_url='login') #meka decorator ekak
def deleteRoom(request, pk):
       room = Rooms.objects.get(id=pk)

       if request.user != room.host:
              return HttpResponse('You are not allowed here!!')

       if request.method == 'POST':
              room.delete()
              return redirect('home')
       return render (request, "base/delete.html" , {'obj': room} )

@login_required(login_url='login')
def deleteMessage(request, pk):
       message = Message.objects.get(id=pk)

       if request.user != message.user:
              return HttpResponse('You are not allowed here!!')

       if request.method == 'POST':
              message.delete()
              return redirect('home')
       return render (request, "base/delete.html" , {'obj': message} )

#3:51:00
       