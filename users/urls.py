from django.urls import path
from .views import login, profile, register, logout

app_name = "users"
urlpatterns = [
    path("login", login, name="login"),
    path("profile", profile, name="profile"),
    path("register", register, name="register"),
    path("logout", logout, name="logout")
]