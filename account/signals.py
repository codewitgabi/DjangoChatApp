from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Chatter


def create_chatter(sender, instance, created, **kwargs):
	if created:
		chatter = Chatter.objects.create(user= instance)
		chatter.save()
		print(f"{chatter.user.username} created")
		

post_save.connect(create_chatter, sender= User)