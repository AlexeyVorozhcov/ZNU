from django.contrib import admin
from users.models import User, Shops, Roles, Category

# Register your models here.

admin.site.register(User)
admin.site.register(Shops)
admin.site.register(Roles)
admin.site.register(Category)


