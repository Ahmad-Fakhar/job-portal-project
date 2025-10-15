from django.db import models
from django.utils import timezone
from accounts.models import User

class Company(models.Model):
    """Company Model for employer registration"""
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='company_profile')
    company_name = models.CharField(max_length=200)
    registration_number = models.CharField(max_length=100, unique=True)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField()
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    company_logo = models.ImageField(upload_to='company_logos/', blank=True)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    submitted_date = models.DateTimeField(auto_now_add=True)
    approved_date = models.DateTimeField(null=True, blank=True)
    rejection_reason = models.TextField(blank=True)
    
    class Meta:
        db_table = 'companies'
        verbose_name_plural = 'Companies'
    
    def __str__(self):
        return self.company_name
    
    def approve(self):
        """Approve company registration"""
        self.status = 'approved'
        self.approved_date = timezone.now()
        self.save()
    
    def reject(self, reason=''):
        """Reject company registration"""
        self.status = 'rejected'
        self.rejection_reason = reason
        self.save()


class Job(models.Model):
    """Job Posting Model"""
    JOB_TYPE_CHOICES = (
        ('full-time', 'Full Time'),
        ('part-time', 'Part Time'),
        ('contract', 'Contract'),
        ('internship', 'Internship'),
    )
    EXPERIENCE_CHOICES = (
        ('0-1', '0-1 years'),
        ('1-3', '1-3 years'),
        ('3-5', '3-5 years'),
        ('5+', '5+ years'),
    )
    
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='jobs')
    title = models.CharField(max_length=200)
    description = models.TextField()
    requirements = models.TextField()
    responsibilities = models.TextField()
    location = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    category = models.CharField(max_length=100)
    salary_min = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    salary_max = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    experience_required = models.CharField(max_length=20, choices=EXPERIENCE_CHOICES)
    vacancies = models.IntegerField(default=1)
    is_active = models.BooleanField(default=True)
    posted_date = models.DateTimeField(auto_now_add=True)
    deadline = models.DateField(null=True, blank=True)
    views_count = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'jobs'
        ordering = ['-posted_date']
    
    def __str__(self):
        return f"{self.title} - {self.company.company_name}"
    
    def increment_views(self):
        """Increment job view count"""
        self.views_count += 1
        self.save(update_fields=['views_count'])