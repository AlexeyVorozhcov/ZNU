from django.db import models
from users.models import User, Category, Shops
from django.urls import reverse
from comments.models import Comments


# Create your models here.

DICT_OF_FILTERS = {
    "Все активные": "all",
    "Ждут рассмотрения": "resh",
    "Ждут уценки в 1С": "utc",
    "Ждут уценки на витрине": "utc_inshop",
    "Уцененные" : "ok_utc_inshop",
    "Отклоненные": "otkl",
    "Архивные": "arch"}

class FiltersOfZayavok(models.Model):
    label = models.CharField(max_length=30) # Название/отображение на сайте
    link = models.CharField(max_length=10) # как будет отображаться в ссылке
    status1 = models.BooleanField(default=None, null=True)  # одобрено
    status2 = models.BooleanField(default=None, null=True)  # отклонено
    status3 = models.BooleanField(default=None, null=True)  # уценено
    status4 = models.BooleanField(default=None, null=True)  # ценник сменен
    status5 = models.BooleanField(default=None, null=True)  # в архиве
    status6 = models.BooleanField(default=None, null=True)    # остальные поля - резервные
    # is_default_for_users = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    
    class Meta:
        verbose_name_plural = "Фильтры заявок"
        verbose_name = "Фильтр заявок"

    def __str__(self):
        return self.label

class Zayavka(models.Model):
    user = models.ForeignKey(User, default=None, null=True, on_delete=models.PROTECT)
    # shop = models.ForeignKey(Shops, default=None, null=True, on_delete=models.PROTECT)
    data = models.DateField(auto_now_add=True)
    category = models.ForeignKey(Category, on_delete=models.PROTECT)
    code = models.CharField(max_length=10)
    name = models.CharField(max_length=100)
    description = models.TextField()
    clarification = models.TextField()
    foto1 = models.ImageField(upload_to="zayavki/foto", blank=True)
    foto2 = models.ImageField(upload_to="zayavki/foto", blank=True)
    status1 = models.BooleanField(default=False)  # одобрено
    status2 = models.BooleanField(default=False)  # отклонено
    status3 = models.BooleanField(default=False)  # уценено
    status4 = models.BooleanField(default=False)  # ценник сменен
    status5 = models.BooleanField(default=False)  # в архиве
    status6 = models.BooleanField(default=False)    # остальные поля - резервные
    
    clarification_of_manager = models.CharField(max_length=150, blank=True)
    

    class Meta:
        verbose_name_plural = "Заявки"
        verbose_name = "Заявка"

    def __str__(self) -> str:
        return self.name

    def get_absolute_url(self):
        return f'/zayavki/{self.id}'
        # TODO вернуть на страницу заявки detail
    
    def get_count_comments(self):
        return Comments.objects.filter(object_id=self.id).count()
    
    