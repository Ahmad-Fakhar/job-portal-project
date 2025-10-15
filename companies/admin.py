from django.contrib import admin
from .models import Company, Job

@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = ['company_name', 'email', 'city', 'status', 'submitted_date']
    list_filter = ['status', 'city']
    search_fields = ['company_name', 'email', 'registration_number']
    actions = ['approve_companies', 'reject_companies']
    
    def approve_companies(self, request, queryset):
        queryset.update(status='approved')
    approve_companies.short_description = "Approve selected companies"

@admin.register(Job)
class JobAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'city', 'job_type', 'is_active', 'posted_date']
    list_filter = ['job_type', 'is_active', 'city']
    search_fields = ['title', 'company__company_name']
