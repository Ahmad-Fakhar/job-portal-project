from django.shortcuts import redirect
from django.contrib import messages
from functools import wraps

def user_type_required(user_type):
    """Decorator to check user type"""
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                messages.error(request, 'Please login first.')
                return redirect('login')
            
            if request.user.user_type != user_type:
                messages.error(request, 'You do not have permission to access this page.')
                return redirect('home')
            
            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator

def company_approved_required(view_func):
    """Decorator to check if company is approved"""
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.error(request, 'Please login first.')
            return redirect('login')
        
        if request.user.user_type != 'company':
            messages.error(request, 'Only companies can access this page.')
            return redirect('home')
        
        try:
            company = request.user.company_profile
            if company.status != 'approved':
                messages.warning(request, 'Your company registration is pending approval.')
                return redirect('company_dashboard')
        except:
            messages.error(request, 'Company profile not found.')
            return redirect('home')
        
        return view_func(request, *args, **kwargs)
    return wrapper
