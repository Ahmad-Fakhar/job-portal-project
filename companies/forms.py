from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Company, Job
from accounts.models import User

class CompanyRegistrationForm(UserCreationForm):
    """Company Registration Form"""
    company_name = forms.CharField(max_length=200, required=True)
    registration_number = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True)
    phone = forms.CharField(max_length=20, required=True)
    address = forms.CharField(widget=forms.Textarea(attrs={'rows': 3}), required=True)
    city = forms.CharField(max_length=100, required=True)
    state = forms.CharField(max_length=100, required=True)
    website = forms.URLField(required=False)
    company_logo = forms.ImageField(required=False)
    description = forms.CharField(widget=forms.Textarea(attrs={'rows': 5}), required=True)
    
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
    
    def clean_registration_number(self):
        reg_number = self.cleaned_data.get('registration_number')
        if Company.objects.filter(registration_number=reg_number).exists():
            raise forms.ValidationError('This registration number already exists.')
        return reg_number
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.user_type = 'company'
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            # Create Company profile
            Company.objects.create(
                user=user,
                company_name=self.cleaned_data['company_name'],
                registration_number=self.cleaned_data['registration_number'],
                email=self.cleaned_data['email'],
                phone=self.cleaned_data['phone'],
                address=self.cleaned_data['address'],
                city=self.cleaned_data['city'],
                state=self.cleaned_data['state'],
                website=self.cleaned_data.get('website', ''),
                company_logo=self.cleaned_data.get('company_logo'),
                description=self.cleaned_data['description'],
                status='pending'
            )
        return user

class CompanyProfileForm(forms.ModelForm):
    """Company Profile Edit Form"""
    class Meta:
        model = Company
        fields = ['company_name', 'email', 'phone', 'address', 'city', 'state', 
                  'website', 'company_logo', 'description']
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
            'description': forms.Textarea(attrs={'rows': 5}),
        }

class JobForm(forms.ModelForm):
    """Job Posting Form"""
    class Meta:
        model = Job
        fields = ['title', 'description', 'requirements', 'responsibilities', 
                  'location', 'city', 'job_type', 'category', 'salary_min', 
                  'salary_max', 'experience_required', 'vacancies', 'deadline']
        widgets = {
            'description': forms.Textarea(attrs={'rows': 5}),
            'requirements': forms.Textarea(attrs={'rows': 4}),
            'responsibilities': forms.Textarea(attrs={'rows': 4}),
            'deadline': forms.DateInput(attrs={'type': 'date'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        salary_min = cleaned_data.get('salary_min')
        salary_max = cleaned_data.get('salary_max')
        
        if salary_min and salary_max:
            if salary_max < salary_min:
                raise forms.ValidationError('Maximum salary must be greater than minimum salary.')
        
        return cleaned_data
