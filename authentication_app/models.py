from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.

class CustomUser(AbstractUser):
    contact_no = models.CharField(max_length=15, unique=True)
    profile_picture = models.ImageField(upload_to='profile_pictures', blank=True)
    
    def __str__(self):
        return self.email