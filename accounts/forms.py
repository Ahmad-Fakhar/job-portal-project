from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User
from jobs.models import JobSeeker

class JobSeekerRegistrationForm(UserCreationForm):
    """Job Seeker Registration Form"""
    full_name = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    city = forms.CharField(max_length=100, required=True)
    date_of_birth = forms.DateField(
        required=False,
        widget=forms.DateInput(attrs={'type': 'date'})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'jobseeker'
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create JobSeeker profile
            JobSeeker.objects.create(
                user=user,
                full_name=self.cleaned_data['full_name'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address'],
                city=self.cleaned_data['city'],
                date_of_birth=self.cleaned_data.get('date_of_birth')
            )
        return user

class JobSeekerProfileForm(forms.ModelForm):
    """Job Seeker Profile Edit Form"""
    class Meta:
        model = JobSeeker
        fields = ['full_name', 'email', 'phone', 'address', 'city', 'date_of_birth', 
                  'skills', 'education', 'experience', 'resume']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'skills': forms.Textarea(attrs={'rows': 4}),
            'education': forms.Textarea(attrs={'rows': 4}),
            'experience': forms.Textarea(attrs={'rows': 4}),
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
