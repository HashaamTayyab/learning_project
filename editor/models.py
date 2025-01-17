from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Track(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()

class Module(models.Model):
    track = models.ForeignKey(Track, related_name='modules', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

class SubDot(models.Model):
    module = models.ForeignKey(Module, related_name='subdots', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

class Topic(models.Model):
    subdot = models.ForeignKey(SubDot, related_name='topics', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    code = models.TextField(blank=True, null=True)  # For code snippets
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # For image uploads
    audio = models.FileField(upload_to='audio/', blank=True, null=True)  # For audio uploads

class Editor(AbstractUser):
    subscribed_modules = models.ManyToManyField(Module, blank=True)
    is_approved = models.BooleanField(default=False)  # Field to track approval status
    
    # Add related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='editor_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )
    
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='editor_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )
