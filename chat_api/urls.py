from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from . import views


urlpatterns = [
	path("<int:id>/", views.message_handler, name= "messages"),
	#path("send-message/<int:id>/", views.post_message_handler.as_view(), name= "post_messages"),
	path("post/<int:id>/", views.post_message, name= "post"),
	path("chatters/", views.ChatterListView.as_view(), name= "chatters"),
]

urlpatterns = format_suffix_patterns(urlpatterns)