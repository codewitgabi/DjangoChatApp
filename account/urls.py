from django.urls import path
from . import views
from django.contrib.auth import views as auth_views


urlpatterns = [
	path("", views.signup, name= "signup"),
	path("add-friends/", views.add_friends, name= "add_friends"),
	path("complete-add-friend", views.complete_add_friend, name= "complete-add-friend"),
	path("login/",
		auth_views.LoginView.as_view(
		template_name="account/login.html",
		redirect_authenticated_user= True),
		name= "login"
	),
	path("home/<int:id>/<str:username>/", views.home, name= "home"),
	path("chat/<int:id>/<str:username>/", views.chat, name= "chat"),
	path("send-message/<int:id>/<str:username>/", views.sendMessage, name= 'send_message'),
	path("get-message/<int:id>/<str:username>/", views.getMessage, name= "get_message"),
]