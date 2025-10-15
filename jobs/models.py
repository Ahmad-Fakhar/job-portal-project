from django.db import models
from accounts.models import User
from companies.models import Job

class JobSeeker(models.Model):
    """Job Seeker Profile"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='jobseeker_profile')
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    resume = models.FileField(upload_to='resumes/', blank=True)
    skills = models.TextField(blank=True)
    education = models.TextField(blank=True)
    experience = models.TextField(blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    
    class Meta:
        db_table = 'job_seekers'
    
    def __str__(self):
        return self.full_name


class Application(models.Model):
    """Job Application Model"""
    STATUS_CHOICES = (
        ('submitted', 'Submitted'),
        ('under_review', 'Under Review'),
        ('shortlisted', 'Shortlisted'),
        ('interview_scheduled', 'Interview Scheduled'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
    )
    
    job = models.ForeignKey(Job, on_delete=models.CASCADE, related_name='applications')
    applicant = models.ForeignKey(User, on_delete=models.CASCADE, related_name='applications')
    resume = models.FileField(upload_to='application_resumes/')
    cover_letter = models.TextField()
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='submitted')
    applied_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    notes = models.TextField(blank=True)
    
    class Meta:
        db_table = 'applications'
        unique_together = ('job', 'applicant')
        ordering = ['-applied_date']
    
    def __str__(self):
        return f"{self.applicant.username} - {self.job.title}"


class SavedJob(models.Model):
    """Saved/Bookmarked Jobs"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saved_jobs')
    job = models.ForeignKey(Job, on_delete=models.CASCADE)
    saved_date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'saved_jobs'
        unique_together = ('user', 'job')
    
    def __str__(self):
        return f"{self.user.username} saved {self.job.title}"
