from django.db import models
from django.db.models.query import QuerySet
from users.models import Roles, User, Category, Shops
from django.urls import reverse
from comments.models import Comments


# Create your models here.

class FiltersOfZayavok(models.Model):
    label = models.CharField(max_length=30) # Название/отображение на сайте
    link = models.CharField(max_length=10) # как будет отображаться в ссылке
    status1 = models.BooleanField(default=None, null=True)  # одобрено
    status2 = models.BooleanField(default=None, null=True)  # отклонено
    status3 = models.BooleanField(default=None, null=True)  # уценено
    status4 = models.BooleanField(default=None, null=True)  # ценник сменен
    status5 = models.BooleanField(default=None, null=True)  # в архиве
    status6 = models.BooleanField(default=None, null=True)    # остальные поля - резервные
    for_roles = models.ManyToManyField(Roles) # для каких ролей пользователя является дефолтным
    
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

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/zayavki/{self.id}'
        # TODO вернуть на страницу заявки detail
        # def get_absolute_url(self):
        #     return reverse('author-detail', kwargs={'pk': self.pk})
    
    def get_count_comments(self):
        return Comments.objects.filter(object_id=self.id).count()
    
    # def users_queryset(user:User):
    #     """Возвращает пользовательский набор заявок без фильтра, т.е. всех заявок, которые доступны пользователю
        
    #     Если роль пользователя - Магазин, то отбираются все заявки, создателем которых является этот магазин
    #     Если роль пользователя - Менеджер, то отбираются те заявки, категории которых есть в рабочих категориях роли пользователя.
    #     """
    #     if user.role.namerole == "Магазин":
    #         return Zayavka.objects.filter(user__shop=user.shop).order_by("-id")
    #     else:
    #         return Zayavka.objects.filter(category__in=user.role.work_category.all()).order_by("-id")
        
    # def users_queryset_onfilter(user:User, filter_:FiltersOfZayavok):
    #     """ Возвращает queryset из пользовательского набора заявок, соответствующих filter_, отсортированных по убыванию id"""
    #     users_queryset = Zayavka.users_queryset(user)
    #     return users_queryset.filter(
    #             status1__in=[True,False] if filter_.status1==None else  [filter_.status1],
    #             status2__in=[True,False] if filter_.status2==None else  [filter_.status2],
    #             status3__in=[True,False] if filter_.status3==None else  [filter_.status3],
    #             status4__in=[True,False] if filter_.status4==None else  [filter_.status4],
    #             status5__in=[True,False] if filter_.status5==None else  [filter_.status5],
    #             status6__in=[True,False] if filter_.status6==None else  [filter_.status6]
    #             ).order_by("-id")
    
     
    
