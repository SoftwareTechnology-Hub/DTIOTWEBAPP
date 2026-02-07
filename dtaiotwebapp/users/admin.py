from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser

# Register your custom user model
admin.site.register(CustomUser)

# Register API key model
