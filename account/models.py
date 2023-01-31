from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
	username        = models.CharField(max_length= 100)
	email               = models.EmailField(unique= True)
	
	REQUIRED_FIELDS = ["username"]
	USERNAME_FIELD = "email"
	
	def __str__(self):
		return self.username
		

class Chatter(models.Model):
	user = models.OneToOneField(User, on_delete= models.CASCADE)
	image = models.ImageField(upload_to= "db_images/", default= "img/download.png")
	friends = models.ManyToManyField("self")
	
	def __str__(self):
		return self.user.username
	
	@property
	def recent_message(self):
		print(dir(self))
		
		
class Message(models.Model):
	sender = models.ForeignKey(Chatter, on_delete= models.CASCADE, related_name= "sender")
	receiver = models.ForeignKey(Chatter, on_delete= models.CASCADE, related_name= "receiver")
	message = models.TextField()
	date_created = models.DateField(auto_now_add= True)
	
	def __str__(self):
		return self.message		
		
