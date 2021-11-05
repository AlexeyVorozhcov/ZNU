from django.urls import path
from zayavki.views import page_view, add_zayavka

app_name = "zayavki"

urlpatterns = [
    path("", page_view, name="page_view"),
    # path('<str:filter>/', page_view, name='page_view_filter'),
    # path('page/<int:page>/', page_view, name='page'),
    path("add_zayavka", add_zayavka, name="add_zayavka"),
]
