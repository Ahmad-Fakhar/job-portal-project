from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('companies/', views.company_list, name='admin_company_list'),
    path('companies//', views.company_detail, name='admin_company_detail'),
    path('companies//approve/', views.company_approve, name='company_approve'),
    path('companies//reject/', views.company_reject, name='company_reject'),
    path('jobs/', views.admin_job_list, name='admin_job_list'),
]
