from django.contrib import admin
from .models import Comments

# Register your models here.

@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ("object_id","created", "autor_id", "body")
    