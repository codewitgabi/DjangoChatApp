from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseAdmin
from .models import *

@admin.register(User)
class UserAdmin(BaseAdmin):
	add_fieldsets = (
		(None, {
			"classes": ("wide",),
			"fields": ("username", "email", "password1", "password2")
		}),
	)
	
	list_display = ("username", "email")
	

admin.site.register(Chatter)
admin.site.register(Message)
