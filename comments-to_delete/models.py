# from django.db import models

# # Create your models here.
# class Comments(models.Model):
#     object_id = models.PositiveSmallIntegerField(null=True)  # id объекта, к которому будут относиться комментарии, например, Заявки
#     created = models.DateTimeField(auto_now_add=True) # дата и время создания комментария
#     autor =models.CharField(max_length=50, default="") # id пользователя, который является автором комментария
#     body = models.TextField(null=True) # текст комментария
#     active = models.BooleanField(default=True) # для отключения неприемлемых комментариев

#     class Meta:
#             verbose_name_plural = "Комментарии"
#             verbose_name = "Комментарий"
    
#     def __str__(self) -> str:
#         return self.body
