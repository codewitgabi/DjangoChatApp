from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import auth
from django.contrib import messages
from django.http import HttpResponse, JsonResponse
from django.contrib.auth import get_user_model
from verify_email.email_handler import send_verification_email
from django.db.models import Q
from .models import Chatter, Message
from .forms import (RegisterForm,
	ChatterUpdateForm,
	UserUpdateForm,
	CustomAdminPasswordChangeForm,
	CustomPasswordChangeForm)
from django.contrib.auth import update_session_auth_hash

from social_django.models import UserSocialAuth
import json


User = get_user_model()


def is_authenticated(func):
	def wrapper(request):
		if request.user.is_authenticated:
			return redirect("home", id= request.user.id, username= request.user.username)
		return func(request)
	return wrapper
	
	
def is_account_owner(func):
	def wrapper(request, id):
		if request.user.id == id:
			return func(request, id)
		return HttpResponse("Can't view this page")
	return wrapper
	
	
def signup_redirect(request):
	return render(request, "account/verify-email.html")
	

@is_authenticated
def signup(request):
	form = RegisterForm()
	if request.method == 'POST':
		form = RegisterForm(request.POST)
		if form.is_valid():
			inactive_user = send_verification_email(request, form)
			return redirect("verify-email")
	return render(request, 'account/signup.html', {"form": form})


@login_required(login_url= "login")
def home(request, id, username):
	user = User.objects.get(id= id, username= request.user.username)
	user = Chatter.objects.get(user= user)
	friends = user.friends.all()
	context = {
		"friends": friends,
	}
	return render(request, "account/home.html", context)
	

@login_required(login_url="login")
def add_friends(request):
	user = request.user
	chatter_obj = Chatter.objects.get(user= user)
	friends = []
	for data in Chatter.objects.all():
		if not data in chatter_obj.friends.all() and data != chatter_obj:
			friends.append(data)
			
	return render(request, "account/add-friend.html", {"friends": friends})
	

@login_required(login_url="login")
@is_account_owner
def update(request, id):
	user = get_object_or_404(User, id=id)
	chatter = user.chatter
	
	form1 = ChatterUpdateForm(request.POST or None,
		request.FILES, instance=chatter)
	form2 = UserUpdateForm(
		request.POST or None, instance=user)
		
	if form1.is_valid() and form2.is_valid():
		form1.save()
		form2.save()
		
	return render(request, "account/update-profile.html", {"form1": form1, "form2": form2})
	
	
def complete_add_friend(request):
	data = json.loads(request.body)
	user_obj = User.objects.get(id=data.get("friend"))
	chatter_obj = Chatter.objects.get(user= user_obj)
	c = Chatter.objects.get(user=request.user)
	c.friends.add(chatter_obj)
	return JsonResponse("added", safe= False)
	
	
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


@login_required(login_url="login")
def settings_view(request):
	user = request.user
	try:
		github_login = user.social_auth.get(provider='github')
	except UserSocialAuth.DoesNotExist:
		github_login = None
			
	try:
		twitter_login = user.social_auth.get(provider='twitter')
	except UserSocialAuth.DoesNotExist:
		twitter_login = None
		
	try:
		facebook_login = user.social_auth.get(provider='facebook')
	except UserSocialAuth.DoesNotExist:
		facebook_login = None
			
	can_disconnect = (user.social_auth.count() > 1 or user.has_usable_password())
		
	return render(request, 'account/settings.html', {
		'github_login': github_login,
		'twitter_login': twitter_login,
		'facebook_login': facebook_login,
		'can_disconnect': can_disconnect
	})
		

@login_required
def password(request):
	if request.user.has_usable_password():
		PasswordForm = CustomPasswordChangeForm
	else:
		PasswordForm = CustomAdminPasswordChangeForm
		
	form = PasswordForm(request.user)
	if request.method == 'POST':
		form = PasswordForm(request.user, request.POST)
		if form.is_valid():
			form.save()
			update_session_auth_hash(request, form.user)
			messages.success(request, 'Your password was successfully updated!')
			return redirect("login")
		else:
			messages.error(request, 'Please correct the error below.')
	return render(request, 'account/password.html', {'form': form})
	
	