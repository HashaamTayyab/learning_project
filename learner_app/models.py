from django.db import models
from authentication_app.models import CustomUser
# Create your models here.

class Track(models.Model):
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
        
class Dot(models.Model):
    name = models.CharField(max_length=30, unique=True, null=False)
    user = models.ManyToManyField(CustomUser, related_name='dots')
    order = models.PositiveIntegerField(default=0)  # Allows manual ordering
    
    class Meta:
        ordering = ['order']  # Orders by the 'order' field
    
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

class Content(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    last_time_edited = models.DateTimeField(auto_now=True)
    content_type = models.CharField(max_length=50)
    sub_dot = models.ForeignKey(SubDot, on_delete=models.CASCADE, related_name='contents')
    view_count = models.IntegerField(default=0)
    rating = models.FloatField(default=0)

    class Meta:
        ordering = ['order']
        
    def __str__(self):
        return self.title


class User(AbstractUser):
    contact_number = models.CharField(max_length=15)
    registration_date = models.DateTimeField(auto_now_add=True)
    profile_picture = models.ImageField(upload_to='profile_pictures/', null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    subscription_type = models.CharField(max_length=50)

    # Many-to-Many Relationships
    tracks_id = models.ManyToManyField(Track, related_name='learners')
    progress_id = models.ManyToManyField('Progress', related_name='learners')
    badges_id = models.ManyToManyField('Badges', related_name='learners')
    subdots_id = models.ManyToManyField(SubDot, related_name='learners')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Assessment(models.Model):
    name = models.CharField(max_length=100)
    sub_dot = models.ForeignKey(SubDot, on_delete=models.CASCADE, related_name='assessments')
    learner_id = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='assessments')

    def __str__(self):
        return self.name


class Feedback(models.Model):
    learner_id = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='feedbacks')
    comments = models.TextField()
    rating = models.FloatField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Feedback by {self.learner}"


class Payment(models.Model):
    learner_id = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50)

    def __str__(self):
        return f"Payment {self.payment_id}"


class ChatHistory(models.Model):
    learner_id = models.ForeignKey(Learner, on_delete=models.CASCADE, related_name='chats')
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.chat_id}"


class Progress(models.Model):
    progress_id = models.CharField(max_length=50, primary_key=True)
    completion_time = models.DateTimeField()
    completion_status = models.CharField(max_length=50)

    def __str__(self):
        return f"Progress {self.progress_id}"


class Badges(models.Model):
    badge_id = models.CharField(max_length=50, primary_key=True)
    title = models.CharField(max_length=100)
    earned_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
