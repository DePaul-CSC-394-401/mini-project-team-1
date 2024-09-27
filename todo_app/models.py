from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Task(models.Model):

    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High')
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    task_name = models.CharField(max_length=200)
    task_description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    due_date = models.DateTimeField(blank=True, null=True)
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    reminder_hours = models.IntegerField(default=24) #default reminder time is 24 hours
    
    def __str__(self):
        return self.task_name
    
    class Meta:
        ordering = ['completed']
    
