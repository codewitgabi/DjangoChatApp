from django.db.models.signals import post_save
from django.contrib.auth import get_user_model
from .models import Chatter

User = get_user_model()

def create_chatter(sender, instance, created, **kwargs):
	if created:
		chatter = Chatter.objects.create(user= instance)
		chatter.save()
		print(f"{chatter.user.username} created")
		

post_save.connect(create_chatter, sender= User)