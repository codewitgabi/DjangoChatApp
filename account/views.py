from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from .models import Chatter, Message
from .forms import RegisterForm
import json


User = get_user_model()


def is_authenticated(func):
	def wrapper(request):
		if request.user.is_authenticated:
			return redirect("home", id= request.user.id, username= request.user.username)
		return func(request)
	return wrapper
	

@is_authenticated
def signup(request):
	form = RegisterForm()
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			password1 = form.cleaned_data.get("password1")
			password2 = form.cleaned_data.get("password2")
			if password1 == password2:
				form.save()			
				return redirect("login")
			else:
				messages.info(request, "Passwords do not match")
				return redirect("signup")
		else:
			username = form.cleaned_data.get("username")
			email = form.cleaned_data.get("email")
			
			if User.objects.filter(username=username).exists():
				messages.info(request, f"User with username {username} already exists!")
				return redirect("signup")
				
			if User.objects.filter(email=email).exists():
				messages.info(request, f"User with email {email} already exists!")
				return redirect("signup")
	
	return render(request, 'account/signup.html', {"form": form})
	

@is_authenticated
def login(request):
	form = RegisterForm()
	if request.method == 'POST':
		username = request.POST.get('username')
		password = request.POST.get('password')
		
		user = auth.authenticate(username= username, password= password)
		
		if user is not None:
			auth.login(request, user)
			return redirect("home", id= request.user.id, username= request.user.username)
		else:
			messages.error(request, 'Incorrect username or password')
			return redirect('login')
	return render(request, 'account/login.html', {"form": form})
	

@login_required(login_url= "login")
def home(request, id, username):
	user = User.objects.get(id= id, username= request.user.username)
	user = Chatter.objects.get(user= user)
	friends = user.friends.all()
	context = {
		"friends": friends,
	}
	return render(request, "account/home.html", context)
	
	
@login_required(login_url= "login")
def chat(request, id, username):
	sender = Chatter.objects.get(user= request.user)
	receiver = User.objects.get(id= id, username= username)
	receiver = Chatter.objects.get(user= receiver)
	
	sender_msg = Message.objects.filter(sender= sender, receiver= receiver)
	receiver_msg = Message.objects.filter(receiver= sender, sender= receiver)
	
	chat_messages = sender_msg.union(receiver_msg).order_by("date_created")
	
	context = {
		"chat_messages": chat_messages,
		"id": id,
		"uname": username,
		"friend": receiver,
	}
	
	return render(request, "account/chat.html", context)
	
	
def sendMessage(request, id, username):
	sender = Chatter.objects.get(user= request.user)
	receiver = User.objects.get(id= id, username= username)
	receiver = Chatter.objects.get(user= receiver)
	
	data = json.loads(request.body)
	message = data.get("message")
	
	print(message)
	
	Message.objects.create(
		sender= sender,
		receiver= receiver,
		message= message
	)
		
	return JsonResponse("message sent", safe= False)
	

def getMessage(request, id, username):
	sender = Chatter.objects.get(user= request.user)
	receiver = User.objects.get(id= id, username= username)
	receiver = Chatter.objects.get(user= receiver)
	
	sender_messages = Message.objects.filter(
		sender= sender,
		receiver= receiver)
	receiver_messages = Message.objects.filter(
		sender= receiver,
		receiver= sender)
	
	db_messages = sender_messages.union(
		receiver_messages).order_by("date_created")
	
	db_messages = list(db_messages.values())
	
	chat_messages = []
	
	for message in db_messages:
		message["sender_id"] = User.objects.get(id= message["sender_id"]).username
		#message["date_created"] = str(message["date_created"])[:5]
		chat_messages.append(message)
		
	return JsonResponse({
		"chat_messages": chat_messages}, safe= False)