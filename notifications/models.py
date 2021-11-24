from django.db import models
from users.models import User
from zayavki.models import Zayavka

# Create your models here.
class Notifications(models.Model):
    created = models.DateField(auto_now_add=True)
    recipient = models.ManyToManyField(User, default=None)
    zayavka = models.ForeignKey(Zayavka, default=None, null=True, on_delete=models.PROTECT)
    text = models.CharField(max_length=250)

    
    class Meta:
        verbose_name_plural = "Уведомления"
        verbose_name = "Уведомление"

    def __str__(self):
        return self.text
    
def create_notification(recipient, zayavka, type_):
    text=""
    if type=="create":
        text = f"Магазин {zayavka.user.shop} создал новую заявку на уценку товара {zayavka.name}."
    Notifications.objects.create(recipient=recipient, zayavka=zayavka, text=text)