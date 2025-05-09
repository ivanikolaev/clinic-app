from django.contrib import admin
from django.utils.translation import gettext_lazy as _
from .models import (
    Department, Doctor, Schedule, Patient, 
    Appointment, MedicalRecord, UserProfile
)

class ScheduleInline(admin.TabularInline):
    model = Schedule
    extra = 1

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'floor', 'room_number')
    search_fields = ('name', 'description', 'phone', 'email')
    list_filter = ('floor',)

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'specialization', 'experience', 'department')
    list_filter = ('specialization', 'department', 'experience')
    search_fields = ('last_name', 'first_name', 'middle_name', 'specialization')
    inlines = [ScheduleInline]
    fieldsets = (
        (_('Личная информация'), {
            'fields': ('last_name', 'first_name', 'middle_name', 'photo', 'bio')
        }),
        (_('Профессиональная информация'), {
            'fields': ('specialization', 'experience', 'department', 'education')
        }),
        (_('Учетная запись'), {
            'fields': ('user',),
            'classes': ('collapse',)
        }),
    )

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'day_of_week', 'start_time', 'end_time', 'is_working_day')
    list_filter = ('day_of_week', 'is_working_day', 'doctor')
    search_fields = ('doctor__last_name', 'doctor__first_name')

@admin.register(Patient)
class PatientAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'date_of_birth', 'phone_number', 'insurance_number')
    list_filter = ('date_of_birth',)
    search_fields = ('last_name', 'first_name', 'middle_name', 'phone_number', 'insurance_number')
    fieldsets = (
        (_('Личная информация'), {
            'fields': ('last_name', 'first_name', 'middle_name', 'date_of_birth')
        }),
        (_('Контактная информация'), {
            'fields': ('phone_number', 'email', 'address')
        }),
        (_('Медицинская информация'), {
            'fields': ('insurance_number',)
        }),
        (_('Учетная запись'), {
            'fields': ('user',),
            'classes': ('collapse',)
        }),
    )

class MedicalRecordInline(admin.StackedInline):
    model = MedicalRecord
    can_delete = False
    verbose_name_plural = _('Медицинская запись')

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status')
    list_filter = ('status', 'date', 'doctor')
    search_fields = ('patient__last_name', 'doctor__last_name', 'reason')
    date_hierarchy = 'date'
    inlines = [MedicalRecordInline]
    fieldsets = (
        (_('Информация о приеме'), {
            'fields': ('patient', 'doctor', 'date', 'time', 'status')
        }),
        (_('Дополнительная информация'), {
            'fields': ('reason', 'notes'),
            'classes': ('collapse',)
        }),
    )

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'created_at')
    search_fields = ('appointment__patient__last_name', 'diagnosis', 'treatment')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        (_('Информация о приеме'), {
            'fields': ('appointment',)
        }),
        (_('Медицинская информация'), {
            'fields': ('diagnosis', 'treatment', 'recommendations')
        }),
        (_('Метаданные'), {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('user__username', 'user__email')
