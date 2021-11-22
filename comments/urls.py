from django.urls import path

from comments.views import add_comment
# from zayavki.views import ZayavkaUpdate, ZayavkaDetail, ZayavkaCreate, ZayavkaFilterList, process_command



app_name = "comments"

urlpatterns = [
    path("", add_comment, name="add-comment"),
    # path('<str:filter>/', ZayavkaFilterList.as_view(), name='zayavki_filter_list'),    
    # path("create", ZayavkaCreate.as_view(), name="zayavka-create"),
    # path("<int:pk>", ZayavkaDetail.as_view(), name="zayavka-detail"),
    # path("<int:pk>/update", ZayavkaUpdate.as_view(), name="zayavka-update"),
    # path("command", process_command, name="zayavka-command"),
    
    
]