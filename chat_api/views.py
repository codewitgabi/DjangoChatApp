from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import generics
from .serializers import MessageSerializer
from account.models import Message, Chatter


@api_view(["GET"])
def message_handler(request, id, format= None):
	if request.method == "GET":
		receiver = Chatter.objects.get(id= id)
		sender = Chatter.objects.get(id= request.user.id)
		
		sender_messages = Message.objects.filter(
			sender= sender,
			receiver= receiver)
		receiver_messages = Message.objects.filter(
			sender= receiver,
			receiver= sender)
			
		chat_messages = sender_messages.union(
		receiver_messages).order_by("date_created")
		
		serializer = MessageSerializer(chat_messages, many= True)
		
		return Response(serializer.data, status= status.HTTP_200_OK)
		

class post_message_handler(generics.CreateAPIView):
	lookup_field = "id"
	queryset = Message.objects.all()
	serializer_class = MessageSerializer
	
	def perform_create(self, serializer):
		print(self.kwargs.get(self.lookup_url_kwarg))
		sender = Chatter.objects.get(id= self.request.user.id)
		receiver = Chatter.objects.get(id= 2)
		serializer.save(sender= sender, receiver= receiver)