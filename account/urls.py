from django.urls import path
from . import views


urlpatterns = [
	path("", views.signup, name= "signup"),
	path("login/", views.login, name= "login"),
	path("home/<int:id>/<str:username>/", views.home, name= "home"),
	path("chat/<int:id>/<str:username>/", views.chat, name= "chat"),
	path("send-message/<int:id>/<str:username>/", views.sendMessage, name= 'send_message'),
	path("get-message/<int:id>/<str:username>/", views.getMessage, name= "get_message"),
]