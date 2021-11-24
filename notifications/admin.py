from django.contrib import admin
from .models import Notifications

# Register your models here.
@admin.register(Notifications)
class NotificationsAdmin(admin.ModelAdmin):
    list_display = ("text",) 