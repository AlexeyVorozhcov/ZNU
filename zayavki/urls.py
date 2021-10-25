from django.urls import path
from zayavki.views import main_page

app_name = "zayavki"

urlpatterns = [
    path("", main_page, name="main_page")
]