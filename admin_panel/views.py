from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q
from companies.models import Company, Job
from jobs.models import Application, JobSeeker
from accounts.models import User
from accounts.decorators import user_type_required
from notifications.models import Notification

@login_required
@user_type_required('admin')
def admin_dashboard(request):
    """Admin dashboard with statistics"""
    total_companies = Company.objects.count()
    pending_companies = Company.objects.filter(status='pending').count()
    approved_companies = Company.objects.filter(status='approved').count()
    total_jobs = Job.objects.count()
    active_jobs = Job.objects.filter(is_active=True).count()
    total_applications = Application.objects.count()
    total_jobseekers = JobSeeker.objects.count()
    
    recent_companies = Company.objects.order_by('-submitted_date')[:5]
    recent_jobs = Job.objects.order_by('-posted_date')[:5]
    
    context = {
        'total_companies': total_companies,
        'pending_companies': pending_companies,
        'approved_companies': approved_companies,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applications': total_applications,
        'total_jobseekers': total_jobseekers,
        'recent_companies': recent_companies,
        'recent_jobs': recent_jobs,
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
@user_type_required('admin')
def company_list(request):
    """List all companies with filters"""
    companies = Company.objects.all().order_by('-submitted_date')
    
    # Filter by status
    status = request.GET.get('status')
    if status:
        companies = companies.filter(status=status)
    
    # Search
    search = request.GET.get('search')
    if search:
        companies = companies.filter(
            Q(company_name__icontains=search) |
            Q(email__icontains=search)
        )
    
    return render(request, 'admin/company_list.html', {'companies': companies})

@login_required
@user_type_required('admin')
def company_detail(request, pk):
    """View company details"""
    company = get_object_or_404(Company, pk=pk)
    jobs = company.jobs.all()
    
    return render(request, 'admin/company_detail.html', {'company': company, 'jobs': jobs})

@login_required
@user_type_required('admin')
def company_approve(request, pk):
    """Approve company"""
    company = get_object_or_404(Company, pk=pk)
    company.approve()
    
    # Send email notification
    try:
        send_mail(
            'Company Registration Approved',
            f'Congratulations! Your company "{company.company_name}" has been approved. You can now login and post jobs.',
            settings.EMAIL_HOST_USER,
            [company.email],
            fail_silently=True,
        )
    except:
        pass
    
    # Create notification
    Notification.objects.create(
        user=company.user,
        title='Company Approved',
        message=f'Your company "{company.company_name}" has been approved!',
        notification_type='approval'
    )
    
    messages.success(request, f'Company "{company.company_name}" approved successfully!')
    return redirect('admin_company_list')

@login_required
@user_type_required('admin')
def company_reject(request, pk):
    """Reject company"""
    company = get_object_or_404(Company, pk=pk)
    
    if request.method == 'POST':
        reason = request.POST.get('reason', 'No reason provided')
        company.reject(reason)
        
        # Send email notification
        try:
            send_mail(
                'Company Registration Rejected',
                f'Your company registration has been rejected. Reason: {reason}',
                settings.EMAIL_HOST_USER,
                [company.email],
                fail_silently=True,
            )
        except:
            pass
        
        messages.success(request, f'Company "{company.company_name}" rejected.')
        return redirect('admin_company_list')
    
    return render(request, 'admin/company_reject.html', {'company': company})

@login_required
@user_type_required('admin')
def admin_job_list(request):
    """List all jobs with filters"""
    jobs = Job.objects.all().order_by('-posted_date')
    
    # Filter by status
    status = request.GET.get('status')
    if status == 'active':
        jobs = jobs.filter(is_active=True)
    elif status == 'inactive':
        jobs = jobs.filter(is_active=False)
    
    # Search
    search = request.GET.get('search')
    if search:
        jobs = jobs.filter(
            Q(title__icontains=search) |
            Q(company__company_name__icontains=search)
        )
    
    return render(request, 'admin/job_list.html', {'jobs': jobs})

