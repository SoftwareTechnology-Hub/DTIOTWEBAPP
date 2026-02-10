from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import CustomUser

# Register your custom user model
admin.site.register(CustomUser)

# Register API key model
from django.contrib import admin
from .models import Notification

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "is_active", "created_at")
    list_filter = ("is_active",)
