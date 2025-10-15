from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('register/', views.jobseeker_register, name='jobseeker_register'),
    path('profile/', views.jobseeker_profile, name='jobseeker_profile'),
]
