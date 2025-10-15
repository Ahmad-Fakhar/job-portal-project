from django import forms
from .models import Application
from companies.models import Job

class ApplicationForm(forms.ModelForm):
    """Job Application Form"""
    class Meta:
        model = Application
        fields = ['resume', 'cover_letter']
        widgets = {
            'cover_letter': forms.Textarea(attrs={
                'rows': 8, 
                'class': 'form-control',
                'placeholder': 'Write your cover letter here...'
            }),
            'resume': forms.FileInput(attrs={
                'class': 'form-control'
            })
        }
    
    def clean_resume(self):
        resume = self.cleaned_data.get('resume')
        if resume:
            # Check file size (5MB max)
            if resume.size > 5 * 1024 * 1024:
                raise forms.ValidationError('Resume file size must not exceed 5MB.')
            
            # Check file extension
            if not resume.name.endswith('.pdf'):
                raise forms.ValidationError('Only PDF files are allowed.')
        
        return resume
    
    def clean_cover_letter(self):
        cover_letter = self.cleaned_data.get('cover_letter')
        if len(cover_letter) < 100:
            raise forms.ValidationError('Cover letter must be at least 100 characters long.')
        return cover_letter

class JobSearchForm(forms.Form):
    """Job Search and Filter Form"""
    keyword = forms.CharField(max_length=200, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Job title, keywords...'
    }))
    location = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Location'
    }))
    job_type = forms.ChoiceField(
        choices=[('', 'All Types')] + list(Job.JOB_TYPE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    experience = forms.ChoiceField(
        choices=[('', 'All Levels')] + list(Job.EXPERIENCE_CHOICES),
        required=False,
        widget=forms.Select(attrs={'class': 'form-select'})
    )
    category = forms.CharField(max_length=100, required=False, widget=forms.TextInput(attrs={
        'class': 'form-control',
        'placeholder': 'Category'
    }))