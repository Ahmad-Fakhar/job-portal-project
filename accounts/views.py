from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import JobSeekerRegistrationForm, JobSeekerProfileForm
from .decorators import user_type_required

def user_login(request):
    """User login view"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'Welcome back, {user.username}!')
            
            # Redirect based on user type
            if user.user_type == 'admin':
                return redirect('admin_dashboard')
            elif user.user_type == 'company':
                return redirect('company_dashboard')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'accounts/login.html')

def user_logout(request):
    """User logout view"""
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('home')

def jobseeker_register(request):
    """Job seeker registration"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = JobSeekerRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful! Welcome aboard.')
            return redirect('jobseeker_profile')
    else:
        form = JobSeekerRegistrationForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
@user_type_required('jobseeker')
def jobseeker_profile(request):
    """Job seeker profile view/edit"""
    try:
        profile = request.user.jobseeker_profile
    except:
        messages.error(request, 'Profile not found.')
        return redirect('home')
    
    if request.method == 'POST':
        form = JobSeekerProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('jobseeker_profile')
    else:
        form = JobSeekerProfileForm(instance=profile)
    
    return render(request, 'accounts/profile.html', {'form': form, 'profile': profile})

