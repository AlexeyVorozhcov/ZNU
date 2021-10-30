from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    role = models.CharField(max_length=50)
    image = models.ImageField(upload_to='users_images', blank=True)