from account.models import User, Chatter
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.forms import AdminPasswordChangeForm, PasswordChangeForm


class RegisterForm(UserCreationForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["password1"].help_text = None
		self.fields["password2"].help_text = None
	
	class Meta:
		model = User
		fields = ["username", "email", "password1", "password2"]


class ChatterUpdateForm(forms.ModelForm):
	class Meta:
		model = Chatter
		fields = ["image"]
		
		
class UserUpdateForm(forms.ModelForm):
	class Meta:
		model = User
		fields = [
			"username",
			"email",
			"first_name",
			"last_name",
		]
		

class CustomAdminPasswordChangeForm(
	AdminPasswordChangeForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		self.fields["password1"].help_text = None
		self.fields["password2"].help_text = None
		
	class Meta:
		model = User
		fields = "__all__"
		

class CustomPasswordChangeForm(PasswordChangeForm):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)
		print(self.fields)
		self.fields["old_password"].help_text = None
		self.fields["new_password1"].help_text = None
		self.fields["new_password2"].help_text = None
		
	class Meta:
		model = User
		fields = "__all__"	