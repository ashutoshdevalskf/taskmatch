from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib import admin

class Skill(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    skills = models.ManyToManyField(Skill, blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)

    @property
    def average_rating(self):
        ratings = [app.rating for app in self.user.applications.filter(rating__isnull=False)]
        return sum(ratings) / len(ratings) if ratings else None

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)

class Task(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
    ]
    title = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    latitude = models.FloatField()
    longitude = models.FloatField()
    location = models.CharField(max_length=255)
    available_from = models.DateTimeField()
    available_to = models.DateTimeField()
    payment = models.DecimalField(max_digits=10, decimal_places=2)
    skills = models.ManyToManyField(Skill, blank=True)
    duration_in_minutes = models.PositiveIntegerField()
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_tasks')

class TaskApplication(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='applications')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    applied_at = models.DateTimeField(auto_now_add=True)
    rating = models.PositiveIntegerField(null=True, blank=True)  # rating out of 5


admin.site.register(Skill)
admin.site.register(UserProfile)
admin.site.register(Task)
admin.site.register(TaskApplication)