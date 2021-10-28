from django.urls import path
from zayavki.views import page_view, one_zayavka

app_name = "zayavki"

urlpatterns = [
    path("", page_view, name="page_view"),
    path("one_zayavka/", one_zayavka, name="one_zayavka"),
]