from django.db import models
from django.contrib.auth.models import User

class Task(models.Model):
    task_name = models.CharField(max_length=200)
    task_description = models.TextField(null=True, blank=True)
    completed = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.task_name
    
