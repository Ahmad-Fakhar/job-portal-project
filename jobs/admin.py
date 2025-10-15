from django.contrib import admin
from .models import JobSeeker, Application, SavedJob

@admin.register(JobSeeker)
class JobSeekerAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'email', 'phone', 'city']
    search_fields = ['full_name', 'email']

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ['applicant', 'job', 'status', 'applied_date']
    list_filter = ['status']
    search_fields = ['applicant__username', 'job__title']

@admin.register(SavedJob)
class SavedJobAdmin(admin.ModelAdmin):
    list_display = ['user', 'job', 'saved_date']
