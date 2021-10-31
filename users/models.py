from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.



class Shops(models.Model):
    nameshop = models.CharField(max_length=30)

    class Meta:
        verbose_name_plural = "Магазины"
        verbose_name = "Магазин"

    def __str__(self):
        return self.nameshop    

class User(AbstractUser):
    role = models.CharField(max_length=50)
    image = models.ImageField(upload_to='users_images', blank=True)
    shop = models.ForeignKey(Shops, on_delete=models.PROTECT, null=True, default=None)        