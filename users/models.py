from django.db import models
from django.contrib.auth.models import AbstractUser
# from zayavki.models import FiltersOfZayavok

# Create your models here.



class Shops(models.Model):
    nameshop = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Магазины"
        verbose_name = "Магазин"

    def __str__(self):
        return self.nameshop    

class Category(models.Model):
    name = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Категории"
        verbose_name = "Категория"

    def __str__(self):
        return self.name

class Roles(models.Model):
    namerole = models.CharField(max_length=30)
    work_category = models.ManyToManyField(Category, default=None, blank=True) 
    # default_filter = models.ForeignKey(FiltersOfZayavok, on_delete=models.PROTECT, null=True, default=None, blank=True) 
    class Meta:
        verbose_name_plural = "Роли"
        verbose_name = "Роль"

    def __str__(self):
        return self.namerole

class User(AbstractUser):
    email = models.EmailField(blank=True)
    role = models.ForeignKey(Roles, on_delete=models.PROTECT, null=True, default=None) 
    shop = models.ForeignKey(Shops, on_delete=models.PROTECT, null=True, default=None, blank=True)
           