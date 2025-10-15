from django.db import models
from accounts.models import User

class Notification(models.Model):
    """Notification Model"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_date = models.DateTimeField(auto_now_add=True)
    notification_type = models.CharField(max_length=50)
    
    class Meta:
        db_table = 'notifications'
        ordering = ['-created_date']
    
    def __str__(self):
        return f"{self.user.username} - {self.title}"
    
    def mark_as_read(self):
        """Mark notification as read"""
        self.is_read = True
        self.save()
