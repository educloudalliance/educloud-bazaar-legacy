from django.contrib import admin
from django.contrib.auth import get_user_model
from models import BazaarUser as User
      
# Register your models here.
admin.site.register(User)
