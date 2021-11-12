from django.urls import path
from zayavki.views import ZayavkaUpdate, ZayavkaDetail, ZayavkaCreate, ZayavkaFilterList



app_name = "zayavki"

urlpatterns = [
    path("", ZayavkaFilterList.as_view(), name="zayavki_list"),
    path('<str:filter>/', ZayavkaFilterList.as_view(), name='zayavki_filter_list'),    
    path("create", ZayavkaCreate.as_view(), name="zayavka-create"),
    path("<int:pk>", ZayavkaDetail.as_view(), name="zayavka-detail"),
    path("<int:pk>/update", ZayavkaUpdate.as_view(), name="zayavka-update"),
    
]
