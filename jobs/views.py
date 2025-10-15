from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from companies.models import Job
from .models import Application, SavedJob, JobSeeker
from .forms import ApplicationForm
from accounts.decorators import user_type_required

def home(request):
    """Homepage"""
    featured_jobs = Job.objects.filter(
        is_active=True, 
        company__status='approved'
    ).order_by('-posted_date')[:6]
    
    context = {'featured_jobs': featured_jobs}
    return render(request, 'home.html', context)

def job_list(request):
    """Job listing with search and filters"""
    jobs = Job.objects.filter(is_active=True, company__status='approved')
    
    # Search by keyword
    keyword = request.GET.get('keyword', '')
    if keyword:
        jobs = jobs.filter(
            Q(title__icontains=keyword) |
            Q(description__icontains=keyword) |
            Q(category__icontains=keyword)
        )
    
    # Filter by location
    location = request.GET.get('location', '')
    if location:
        jobs = jobs.filter(Q(city__icontains=location) | Q(location__icontains=location))
    
    # Filter by job type
    job_type = request.GET.get('job_type', '')
    if job_type:
        jobs = jobs.filter(job_type=job_type)
    
    # Filter by experience
    experience = request.GET.get('experience', '')
    if experience:
        jobs = jobs.filter(experience_required=experience)
    
    # Sorting
    sort = request.GET.get('sort', '-posted_date')
    jobs = jobs.order_by(sort)
    
    # Pagination
    paginator = Paginator(jobs, 20)
    page_number = request.GET.get('page')
    jobs_page = paginator.get_page(page_number)
    
    context = {
        'jobs': jobs_page,
        'job_types': Job.JOB_TYPE_CHOICES,
        'experience_levels': Job.EXPERIENCE_CHOICES,
        'keyword': keyword,
        'location': location,
    }
    return render(request, 'jobs/job_list.html', context)

def job_detail(request, pk):
    """Job detail page"""
    job = get_object_or_404(Job, pk=pk, is_active=True)
    job.increment_views()
    
    # Check if user has already applied
    has_applied = False
    is_saved = False
    if request.user.is_authenticated:
        has_applied = Application.objects.filter(job=job, applicant=request.user).exists()
        is_saved = SavedJob.objects.filter(job=job, user=request.user).exists()
    
    context = {
        'job': job,
        'has_applied': has_applied,
        'is_saved': is_saved,
    }
    return render(request, 'jobs/job_detail.html', context)

@login_required
@user_type_required('jobseeker')
def apply_job(request, pk):
    """Apply for a job"""
    job = get_object_or_404(Job, pk=pk, is_active=True)
    
    # Check if already applied
    if Application.objects.filter(job=job, applicant=request.user).exists():
        messages.error(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.applicant = request.user
            application.save()
            
            messages.success(request, 'Application submitted successfully!')
            return redirect('my_applications')
    else:
        form = ApplicationForm()
    
    return render(request, 'jobs/apply.html', {'form': form, 'job': job})

@login_required
@user_type_required('jobseeker')
def my_applications(request):
    """User's application history"""
    applications = Application.objects.filter(
        applicant=request.user
    ).select_related('job', 'job__company').order_by('-applied_date')
    
    return render(request, 'jobs/my_applications.html', {'applications': applications})

@login_required
@user_type_required('jobseeker')
def saved_jobs_view(request):
    """User's saved jobs"""
    saved_jobs = SavedJob.objects.filter(
        user=request.user
    ).select_related('job', 'job__company').order_by('-saved_date')
    
    return render(request, 'jobs/saved_jobs.html', {'saved_jobs': saved_jobs})

@login_required
@require_POST
def save_job(request, pk):
    """Save/unsave a job (AJAX)"""
    job = get_object_or_404(Job, pk=pk)
    saved_job, created = SavedJob.objects.get_or_create(
        user=request.user,
        job=job
    )
    
    if not created:
        # Already saved, so unsave it
        saved_job.delete()
        return JsonResponse({'saved': False})
    
    return JsonResponse({'saved': True})