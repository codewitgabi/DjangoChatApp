from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
import uuid


class User(AbstractUser):
	id = models.UUIDField(
		primary_key=True,
		editable=False,
		default=uuid.uuid4)
	username        = models.CharField(max_length= 100)
	email               = models.EmailField(unique= True)
	
	REQUIRED_FIELDS = ["username"]
	USERNAME_FIELD = "email"
	
	def __str__(self):
		return self.username
		

class Chatter(models.Model):
	id = models.UUIDField(
		primary_key=True,
		editable=False,
		default=uuid.uuid4)
	user = models.OneToOneField(User, on_delete= models.CASCADE)
	image = models.ImageField(upload_to= "db_images/", default= "img/download.png")
	friends = models.ManyToManyField("self")
	
	def __str__(self):
		return self.user.username
	
	@property
	def is_online(self):
		"""
		checks if user has been offline for more than 2 minutes
		bugs:
			this isnt correct.
		"""
		delta = timezone.now() - self.user.last_login
		return delta.seconds < 120
		
		
class Message(models.Model):
	sender = models.ForeignKey(Chatter, on_delete= models.CASCADE, related_name= "sender")
	receiver = models.ForeignKey(Chatter, on_delete= models.CASCADE, related_name= "receiver")
	message = models.TextField()
	date_created = models.DateField(auto_now_add= True)
	
	def __str__(self):
		return self.message		
		
