from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

urlpatterns = [
	path("", views.signup, name= "signup"),
	path("update/<uuid:id>/", views.update, name="update-profile"),
	path("add-friends/", views.add_friends, name= "add_friends"),
	path("verify-email/", views.signup_redirect, name="verify-email"),
	# social auth management
	path("settings/", views.settings_view, name='settings'),
	path("settings/password/", views.password, name="password"),
	path("complete-add-friend", views.complete_add_friend, name= "complete-add-friend"),
	path("login/",
		auth_views.LoginView.as_view(
		template_name="account/login.html",
		redirect_authenticated_user= True),
		name= "login"
	),
	path("logout/",
		auth_views.LogoutView.as_view(),
		name= "logout"
	),
	
	path("home/<uuid:id>/<str:username>/", views.home, name= "home"),
	path("chat/<uuid:id>/<str:username>/", views.chat, name= "chat"),
	path("send-message/<uuid:id>/<str:username>/", views.sendMessage, name= 'send_message'),
	path("get-message/<uuid:id>/<str:username>/", views.getMessage, name= "get_message"),
]