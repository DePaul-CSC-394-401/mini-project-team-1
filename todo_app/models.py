from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MaxValueValidator, MinValueValidator

class Task(models.Model):

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ]

    PERCENTAGES_CHOICES = [
        ("0%", "0%"), ("5%", "5%"), ("10%", "10%"), ("15%", "15%"), ("20%", "20%"), ("25%", "25%"), ("30%", "30%"), ("40%", "40%"), ("50%", "50%"),
        ("60%", "60%"), ("70%", "70%"), ("80%", "80%"), ("90%", "90%"), ("100%", "100%")
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    task_name = models.CharField(max_length=200)
    task_description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    reminder_hours = models.IntegerField(default=24) #default reminder time is 24 hours
    category = models.CharField(max_length=20, default='Uncategorized')
    progress = models.CharField(max_length=5, choices=PERCENTAGES_CHOICES, default="0%")
    
    def __str__(self):
        return self.task_name
    
    class Meta:
        ordering = ['completed']
    
