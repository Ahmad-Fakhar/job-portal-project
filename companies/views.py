from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Company, Job
from .forms import CompanyRegistrationForm, CompanyProfileForm, JobForm
from jobs.models import Application
from accounts.decorators import user_type_required, company_approved_required

def company_register(request):
    """Company registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = CompanyRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Registration successful! Please wait for admin approval.')
            return redirect('login')
    else:
        form = CompanyRegistrationForm()
    
    return render(request, 'company/register.html', {'form': form})

@login_required
@user_type_required('company')
def company_dashboard(request):
    """Company dashboard"""
    try:
        company = request.user.company_profile
    except:
        messages.error(request, 'Company profile not found.')
        return redirect('home')
    
    # Get statistics
    total_jobs = company.jobs.count()
    active_jobs = company.jobs.filter(is_active=True).count()
    total_applications = Application.objects.filter(job__company=company).count()
    recent_applications = Application.objects.filter(job__company=company).order_by('-applied_date')[:5]
    
    context = {
        'company': company,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applications': total_applications,
        'recent_applications': recent_applications,
    }
    return render(request, 'company/dashboard.html', context)

@login_required
@company_approved_required
def job_create(request):
    """Create new job posting"""
    company = request.user.company_profile
    
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.company = company
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('company_job_list')
    else:
        form = JobForm()
    
    return render(request, 'company/job_form.html', {'form': form, 'action': 'Create'})

@login_required
@company_approved_required
def job_edit(request, pk):
    """Edit job posting"""
    job = get_object_or_404(Job, pk=pk, company=request.user.company_profile)
    
    if request.method == 'POST':
        form = JobForm(request.POST, instance=job)
        if form.is_valid():
            form.save()
            messages.success(request, 'Job updated successfully!')
            return redirect('company_job_list')
    else:
        form = JobForm(instance=job)
    
    return render(request, 'company/job_form.html', {'form': form, 'action': 'Edit', 'job': job})

@login_required
@company_approved_required
def company_job_list(request):
    """List company's jobs"""
    company = request.user.company_profile
    jobs = company.jobs.all().order_by('-posted_date')
    
    return render(request, 'company/job_list.html', {'jobs': jobs})

@login_required
@company_approved_required
def application_list(request):
    """View all applications for company"""
    company = request.user.company_profile
    applications = Application.objects.filter(job__company=company).select_related('job', 'applicant')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        applications = applications.filter(status=status)
    
    # Filter by job
    job_id = request.GET.get('job')
    if job_id:
        applications = applications.filter(job_id=job_id)
    
    return render(request, 'company/application_list.html', {
        'applications': applications,
        'company': company
    })

@login_required
@user_type_required('company')
def company_profile(request):
    """Company profile view/edit"""
    try:
        company = request.user.company_profile
    except:
        messages.error(request, 'Company profile not found.')
        return redirect('home')
    
    if request.method == 'POST':
        form = CompanyProfileForm(request.POST, request.FILES, instance=company)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('company_profile')
    else:
        form = CompanyProfileForm(instance=company)
    
    return render(request, 'company/profile.html', {'form': form, 'company': company})

@login_required
@company_approved_required
def job_delete(request, pk):
    """Delete job posting"""
    job = get_object_or_404(Job, pk=pk, company=request.user.company_profile)
    
    if request.method == 'POST':
        job_title = job.title
        job.delete()
        messages.success(request, f'Job "{job_title}" deleted successfully!')
        return redirect('company_job_list')
    
    return render(request, 'company/job_delete_confirm.html', {'job': job})

@login_required
@company_approved_required
def application_detail(request, pk):
    """View application details"""
    application = get_object_or_404(Application, pk=pk, job__company=request.user.company_profile)
    
    if request.method == 'POST':
        status = request.POST.get('status')
        if status in dict(Application.STATUS_CHOICES):
            application.status = status
            application.save()
            messages.success(request, 'Application status updated!')
            return redirect('application_detail', pk=pk)
    
    return render(request, 'company/application_detail.html', {'application': application})