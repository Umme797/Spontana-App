from django.db import models
from django.contrib.auth.models import User

import uuid

# Create your models here.



# USER PROFILE MODEL
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    num_adventures = models.PositiveIntegerField(default=0)
    bio = models.TextField(blank=True)
    image = models.ImageField(upload_to='profile_images/', blank=True, null=True)

    def __str__(self):
        return self.user.username




# ACTIVITY JOURNAL MODEL
class ActivityJournal(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    image = models.ImageField(upload_to='activity_images/')
    title = models.CharField(max_length=100)
    date = models.DateField()
    description = models.TextField()
    mood = models.CharField(max_length=50)
    duration = models.CharField(max_length=50)
    rating = models.PositiveSmallIntegerField(blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.user.username}"



# MOOD TIME ENTRY MODEL
class MoodTimeEntry(models.Model):
    mood = models.CharField(max_length=50)
    duration = models.DurationField()  

    def __str__(self):
        return f"{self.mood} for {self.duration}"



# ACTIVITY SUGGESTION MODEL
class Activity(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    mood_entry = models.ForeignKey(MoodTimeEntry, on_delete=models.SET_NULL, null=True)
    duration = models.DurationField()
    image = models.ImageField(upload_to='activity_suggestions/', blank=True)

    def __str__(self):
        return self.title



# EMAIL VERIFICATION MODEL
class EmailVerification(models.Model):
    email = models.EmailField(unique=True)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email



