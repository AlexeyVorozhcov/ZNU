from django.urls import path
from .views import index

app_name = "users"
urlpatterns = [
    path("login", index, name="login")
]