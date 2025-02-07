from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
import os

# Create your models here.

def user_profile_path(instance, filename):
    # Generate file path for user profile pictures
    ext = filename.split('.')[-1]
    filename = f'{instance.user.username}_profile.{ext}'
    return os.path.join('profile_pics', filename)

class LearnerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.TextField(max_length=500, blank=True)
    profile_picture = models.ImageField(upload_to=user_profile_path, blank=True, null=True)
    learning_style = models.CharField(max_length=20, choices=[
        ('visual', 'Visual'),
        ('auditory', 'Auditory'),
        ('reading', 'Reading/Writing'),
        ('kinesthetic', 'Kinesthetic')
    ], default='visual')
    email_notifications = models.BooleanField(default=True)
    progress_reminders = models.BooleanField(default=True)
    public_profile = models.BooleanField(default=False)
    show_progress = models.BooleanField(default=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"

    @property
    def profile_image_url(self):
        if self.profile_picture:
            return self.profile_picture.url
        return None

class Track(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_completion_status(self, learner):
        total_dots = self.dot_set.count()
        if total_dots == 0:
            return 0
        completed_dots = sum(1 for dot in self.dot_set.all() if dot.is_completed(learner))
        return (completed_dots / total_dots) * 100
    
    def is_completed(self, learner):
        return all(dot.is_completed(learner) for dot in self.dot_set.all())

class Dot(models.Model):
    track = models.ForeignKey(Track, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    order = models.IntegerField()
    
    def get_completion_status(self, learner):
        total_subdots = self.subdot_set.count()
        if total_subdots == 0:
            return 0
        completed_subdots = sum(1 for subdot in self.subdot_set.all() if subdot.is_completed(learner))
        return (completed_subdots / total_subdots) * 100
    
    def is_completed(self, learner):
        return all(subdot.is_completed(learner) for subdot in self.subdot_set.all())

class SubDot(models.Model):
    dot = models.ForeignKey(Dot, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    content = models.TextField()
    code_snippet = models.TextField(blank=True)
    image_url = models.URLField(blank=True)
    order = models.IntegerField()
    
    def is_completed(self, learner):
        try:
            progress = Progress.objects.get(learner=learner, subdot=self)
            return progress.completed
        except Progress.DoesNotExist:
            return False

class Topic(models.Model):
    subdot = models.ForeignKey(SubDot, related_name='topics', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    content = models.TextField()
    code = models.TextField(blank=True, null=True)  # For code snippets
    image = models.ImageField(upload_to='images/', blank=True, null=True)  # For image uploads
    audio = models.FileField(upload_to='audio/', blank=True, null=True)  # For audio uploads
    timestamps = models.JSONField(blank=True, null=True)  # For storing audio timestamps

class Progress(models.Model):
    learner = models.ForeignKey(LearnerProfile, on_delete=models.CASCADE)
    subdot = models.ForeignKey(SubDot, on_delete=models.CASCADE)
    completed = models.BooleanField(default=False)
    completed_at = models.DateTimeField(null=True, blank=True)
    time_spent = models.DurationField(null=True, blank=True)
    last_accessed = models.DateTimeField(auto_now=True)
    start_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = ('learner', 'subdot')
    
class Note(models.Model):
    learner = models.ForeignKey(LearnerProfile, on_delete=models.CASCADE)
    subdot = models.ForeignKey(SubDot, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    
class Bookmark(models.Model):
    learner = models.ForeignKey(LearnerProfile, on_delete=models.CASCADE)
    subdot = models.ForeignKey(SubDot, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
class Assessment(models.Model):
    dot = models.ForeignKey(Dot, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField()
    
class AssessmentResult(models.Model):
    learner = models.ForeignKey(LearnerProfile, on_delete=models.CASCADE)
    assessment = models.ForeignKey(Assessment, on_delete=models.CASCADE)
    score = models.FloatField()
    completed_at = models.DateTimeField(auto_now_add=True)
    
class InstructorQuestion(models.Model):
    learner = models.ForeignKey(LearnerProfile, on_delete=models.CASCADE)
    subdot = models.ForeignKey(SubDot, on_delete=models.CASCADE)
    question = models.TextField()
    answer = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    answered_at = models.DateTimeField(null=True, blank=True)
