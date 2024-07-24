from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    ROLE_CHOICES = [
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('client', 'Client')
    ]
    role = models.CharField(max_length=10, null=True, choices=ROLE_CHOICES)
    
    email = models.EmailField(max_length=255, unique=True)
    username = models.CharField(max_length=150, unique=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email
    
class Task(models.Model):
    STATUS = [
        ('pending','Pending'),
         ('complete','Complete')
    ]
    title = models.CharField(max_length=255)
    description = models.TextField()
    task_date = models.DateField()
    is_completed = models.BooleanField(default=False)
    status = models.CharField(max_length=10, choices=STATUS)
    created_by = models.ForeignKey(User, related_name='tasks_created', on_delete=models.CASCADE)
    assigned_to = models.ForeignKey(User, related_name='tasks_assigned', on_delete=models.CASCADE)

