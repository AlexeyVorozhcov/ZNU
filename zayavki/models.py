from django.db import models
from users.models import User

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"

    def __str__(self) -> str:
        return self.name


class Zayavka(models.Model):
    user = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    data = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    description = models.TextField()
    clarification = models.TextField()
    foto1 = models.ImageField(upload_to="zayavki/foto", blank=True)
    foto2 = models.ImageField(upload_to="zayavki/foto", blank=True)
    status1 = models.BooleanField()  # одобрено
    status2 = models.BooleanField()  # отклонено
    status3 = models.BooleanField()  # уценено
    status4 = models.BooleanField()  # ценник сменен
    status5 = models.BooleanField()  # остальные поля - резервные
    status6 = models.BooleanField()
    clarification_of_manager = models.CharField(max_length=150, blank=True)

    class Meta:
        verbose_name_plural = "Заявки"
        verbose_name = "Заявка"

    def __str__(self) -> str:
        return self.name
