from django.db import models

# Create your models here.
class Comments(models.Model):
    object_id = models.PositiveSmallIntegerField()  # id объекта, к которому будут относиться комментарии, например, Заявки
    created = models.DateTimeField(auto_now_add=True) # дата и время создания комментария
    autor_id =models.PositiveSmallIntegerField() # id пользователя, который является автором комментария
    body = models.TextField() # текст комментария
    active = models.BooleanField(default=True) # для отключения неприемлемых комментариев

    class Meta:
            verbose_name_plural = "Комментарии"
            verbose_name = "Комментарий"
    
    def __str__(self) -> str:
        return self.body
