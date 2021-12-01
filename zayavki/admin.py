from django.contrib import admin
from zayavki.models import Zayavka, FiltersOfZayavok
from .models import Comments2
# from django.db import models

# Register your models here.


admin.site.register(Comments2)

@admin.register(Zayavka)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name","user", "category", "data")
    fields = ("user",  ("code", "name", "category"), "description", "clarification",
    "foto1", "foto2", ("status1", "status2", "status3","status4", "status5", "status6"), 
    "clarification_of_manager")
    

@admin.register(FiltersOfZayavok)
class FiltersOfZayavokAdmin(admin.ModelAdmin):
    list_display = ("id", "label","link", "status1", "status2", "status3", "status4", "status5", "status6")    