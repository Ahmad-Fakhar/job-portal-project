from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    """Custom User Model with user type"""
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('company', 'Company'),
        ('jobseeker', 'Job Seeker'),
    )
    
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)
    profile_image = models.ImageField(upload_to='profiles/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return f"{self.username} ({self.user_type})"
