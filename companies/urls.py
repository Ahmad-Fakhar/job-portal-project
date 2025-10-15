from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.company_register, name='company_register'),
    path('dashboard/', views.company_dashboard, name='company_dashboard'),
    path('profile/', views.company_profile, name='company_profile'),
    path('jobs/', views.company_job_list, name='company_job_list'),
    path('jobs/create/', views.job_create, name='job_create'),
    path('jobs//edit/', views.job_edit, name='job_edit'),
    path('jobs//delete/', views.job_delete, name='job_delete'),
    path('applications/', views.application_list, name='company_application_list'),
    path('applications//', views.application_detail, name='application_detail'),
]
