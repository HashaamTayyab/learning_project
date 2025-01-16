from django.db import models
from authentication_app.models import CustomUser
# Create your models here.

class Dot(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    user = models.ManyToManyField(CustomUser, related_name='dots')
    
    def __str__(self):
        return self.name


class SubDot(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    dot = models.ForeignKey(Dot, on_delete=models.CASCADE, related_name='subdots')
    order = models.PositiveIntegerField(default=0)  # Allows manual ordering

    class Meta:
        ordering = ['order']  # Orders by the 'order' field

    def __str__(self):
        return f"{self.order}: {self.name}"

    