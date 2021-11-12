from django.urls import path
from zayavki.views import ZayavkaList, ZayavkaUpdate, ZayavkaDetail, ZayavkaCreate, ZayavkaFilterList



app_name = "zayavki"

urlpatterns = [
    path("", ZayavkaList.as_view(), name="zayavki_list"),
    path('<str:filter>/', ZayavkaFilterList.as_view(), name='zayavki_filter_list'),
    # path('page/<int:page>/', page_view, name='page'),
    path("create", ZayavkaCreate.as_view(), name="zayavka-create"),
    path("<int:pk>", ZayavkaDetail.as_view(), name="zayavka-detail"),
    path("<int:pk>/update", ZayavkaUpdate.as_view(), name="zayavka-update"),
    
]
