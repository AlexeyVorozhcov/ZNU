from enum import Enum, auto
from django.db import models
from django.db.models import manager
from django.db.models.query import QuerySet
from users.models import Roles, User, Category, Shops
from django.urls import reverse


# Create your models here.

class FiltersOfZayavok(models.Model):
    label = models.CharField(max_length=30)  # Название/отображение на сайте
    link = models.CharField(max_length=10)  # как будет отображаться в ссылке
    status1 = models.BooleanField(default=None, null=True)  # одобрено
    status2 = models.BooleanField(default=None, null=True)  # отклонено
    status3 = models.BooleanField(default=None, null=True)  # уценено
    status4 = models.BooleanField(default=None, null=True)  # ценник сменен
    status5 = models.BooleanField(default=None, null=True)  # в архиве
    # остальные поля - резервные
    status6 = models.BooleanField(default=None, null=True)
    # для каких ролей пользователя является дефолтным
    for_roles = models.ManyToManyField(Roles)

    class Meta:
        verbose_name_plural = "Фильтры заявок"
        verbose_name = "Фильтр заявок"

    def __str__(self):
        return self.label


class Zayavka(models.Model):
    user = models.ForeignKey(
        User, default=None, null=True, on_delete=models.PROTECT)
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
    # остальные поля - резервные
    status6 = models.BooleanField(default=False)
    clarification_of_manager = models.CharField(max_length=150, blank=True)
    manager = models.ForeignKey(
        User, default=None, null=True, on_delete=models.PROTECT, related_name='+')
    # manager - тот, кто последний вносил изменения в статусы

    class Meta:
        verbose_name_plural = "Заявки"
        verbose_name = "Заявка"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/zayavki/{self.id}'
        # TODO вернуть на страницу заявки detail
        # def get_absolute_url(self):
        #     return reverse('author-detail', kwargs={'pk': self.pk})

    def get_count_comments(self):
        return Comments2.objects.filter(object_id=self.id).count()


class Comments2(models.Model):
    # id объекта, к которому будут относиться комментарии, например, Заявки
    object_id = models.PositiveSmallIntegerField(null=True)
    # дата и время создания комментария
    created = models.DateTimeField(auto_now_add=True)
    # id пользователя, который является автором комментария
    autor = models.CharField(max_length=50, default="")
    body = models.TextField(null=True)  # текст комментария
    # для отключения неприемлемых комментариев
    active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Комментарии"
        verbose_name = "Комментарий"

    def __str__(self) -> str:
        return self.body


class EventNotification(Enum):
    CREATE_ZAYAVKA = 'Магазин "#" создал новую заявку на уценку'
    ADD_COMMENT = 'Добавлен новый комментарий в заявку'
    SET_STATUS1_TRUE = 'Менеджер одобрил заявку'
    SET_STATUS2_TRUE = 'Менеджер отклонил заявку'
    SET_STATUS3_TRUE = 'Менеджер перевел товар в качество БУ или Discount'
    SET_STATUS4_TRUE = "4"
    SET_STATUS5_TRUE = "5"


class Notifications2(models.Model):
    created = models.DateField(auto_now_add=True)
    recipient = models.ManyToManyField(User)
    zayavka = models.ForeignKey(
        Zayavka, default=None, null=True, on_delete=models.PROTECT)
    text = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Уведомления"
        verbose_name = "Уведомление"

    def __str__(self):
        return self.text
