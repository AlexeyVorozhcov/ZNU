from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=30)

class Zayavka(models.Model):
    shop = models.CharField(max_length=50) # поменять на ссылку на пользователя
    data = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    description = models.TextField()
    clarification = models.TextField()
    foto1 = models.ImageField(upload_to="zayavki/foto", blank=True )
    foto2 = models.ImageField(upload_to="zayavki/foto", blank=True)
    status1 = models.BooleanField() # менеджер рассмотрел
    status2 = models.BooleanField() # перевод в уценку произведен
    status3 = models.BooleanField() # ценник в магазине изменен
    status4 = models.BooleanField() # доп. - отклонено
    status5 = models.BooleanField() # остальные поля - резервные
    status6 = models.BooleanField()
    clarification_of_manager = models.CharField(max_length=150, blank=True)


