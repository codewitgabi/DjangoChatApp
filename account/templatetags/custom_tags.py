from django import template
from account.models import Chatter, Message
from django.contrib.auth import get_user_model

User = get_user_model()

# register tags
register = template.Library()

@register.inclusion_tag("account/last_message.html")
def display_recent_message(request, friend):
	sender = Chatter.objects.get(user=request.user)
	receiver = Chatter.objects.get(user=User.objects.get(id=friend.id, username=friend))
	
	sender_messages = Message.objects.filter(
		sender= sender,
		receiver= receiver)
		
	receiver_messages = Message.objects.filter(
		sender= receiver,
		receiver= sender)
		
	last_message = sender_messages.union(
		receiver_messages)
		
	print(last_message.last())
		
	return {"last_message": last_message.last()}