from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Основные страницы
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    
    # Аутентификация
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('password-reset/', 
         auth_views.PasswordResetView.as_view(template_name='medical/password_reset.html'), 
         name='password_reset'),
    path('password-reset/done/', 
         auth_views.PasswordResetDoneView.as_view(template_name='medical/password_reset_done.html'), 
         name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/', 
         auth_views.PasswordResetConfirmView.as_view(template_name='medical/password_reset_confirm.html'), 
         name='password_reset_confirm'),
    path('password-reset-complete/', 
         auth_views.PasswordResetCompleteView.as_view(template_name='medical/password_reset_complete.html'), 
         name='password_reset_complete'),
    
    # Профиль пациента
    path('profile/', views.patient_profile, name='patient_profile'),
    path('profile/create/', views.patient_profile_create, name='patient_profile_create'),
    path('profile/update/', views.patient_profile_update, name='patient_profile_update'),
    
    # Отделения
    path('departments/', views.DepartmentListView.as_view(), name='department_list'),
    path('departments/<int:pk>/', views.DepartmentDetailView.as_view(), name='department_detail'),
    
    # Врачи
    path('doctors/', views.doctor_list, name='doctor_list'),
    path('doctors/<int:pk>/', views.DoctorDetailView.as_view(), name='doctor_detail'),
    
    # Записи на прием
    path('appointments/', views.appointment_list, name='appointment_list'),
    path('appointments/<int:pk>/', views.appointment_detail, name='appointment_detail'),
    path('appointments/create/<int:doctor_id>/', views.appointment_create, name='appointment_create'),
    path('appointments/<int:pk>/cancel/', views.appointment_cancel, name='appointment_cancel'),
    
    # API
    path('api/available-slots/', views.get_available_slots, name='api_available_slots'),
    
    # Административные страницы
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
    path('admin-dashboard/appointments/<int:pk>/update/', 
         views.AdminAppointmentUpdateView.as_view(), name='admin_appointment_update'),
]