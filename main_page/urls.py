from django.urls import path
from .views import index

app_name = "main_page"
urlpatterns = [
    path("", index, name="index")
]
