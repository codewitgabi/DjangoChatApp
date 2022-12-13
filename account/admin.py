from django.contrib import admin
from .models import *

admin.site.register(Chatter)
admin.site.register(Message)