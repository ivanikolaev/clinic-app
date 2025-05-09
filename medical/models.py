from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

# Choices for appointment status
STATUS_CHOICES = (
    ('scheduled', 'Запланирован'),
    ('completed', 'Завершен'),
    ('cancelled', 'Отменен'),
    ('no_show', 'Неявка'),
)

class Department(models.Model):
    """Модель отделения поликлиники"""
    name = models.CharField(_('Название'), max_length=100)
    description = models.TextField(_('Описание'))
    phone = models.CharField(_('Телефон'), max_length=20)
    email = models.EmailField(_('Email'), blank=True, null=True)
    floor = models.PositiveSmallIntegerField(_('Этаж'), blank=True, null=True)
    room_number = models.CharField(_('Номер кабинета'), max_length=10, blank=True, null=True)
    
    class Meta:
        verbose_name = _('Отделение')
        verbose_name_plural = _('Отделения')
        ordering = ['name']
    
    def __str__(self):
        return self.name

class Doctor(models.Model):
    """Модель врача поликлиники"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='doctor_profile', null=True, blank=True)
    last_name = models.CharField(_('Фамилия'), max_length=100)
    first_name = models.CharField(_('Имя'), max_length=100)
    middle_name = models.CharField(_('Отчество'), max_length=100, blank=True, null=True)
    specialization = models.CharField(_('Специализация'), max_length=100)
    experience = models.PositiveIntegerField(_('Опыт работы (лет)'))
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='doctors', verbose_name=_('Отделение'))
    photo = models.ImageField(_('Фото'), upload_to='doctors/', blank=True, null=True)
    bio = models.TextField(_('Биография'), blank=True, null=True)
    education = models.TextField(_('Образование'), blank=True, null=True)
    
    class Meta:
        verbose_name = _('Врач')
        verbose_name_plural = _('Врачи')
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''} - {self.specialization}"
    
    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"

class Schedule(models.Model):
    """Модель графика работы врача"""
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='schedules', verbose_name=_('Врач'))
    day_of_week = models.PositiveSmallIntegerField(_('День недели'), choices=(
        (1, 'Понедельник'),
        (2, 'Вторник'),
        (3, 'Среда'),
        (4, 'Четверг'),
        (5, 'Пятница'),
        (6, 'Суббота'),
        (7, 'Воскресенье'),
    ))
    start_time = models.TimeField(_('Время начала'))
    end_time = models.TimeField(_('Время окончания'))
    is_working_day = models.BooleanField(_('Рабочий день'), default=True)
    
    class Meta:
        verbose_name = _('График работы')
        verbose_name_plural = _('Графики работы')
        ordering = ['doctor', 'day_of_week', 'start_time']
        unique_together = ['doctor', 'day_of_week']
    
    def __str__(self):
        return f"{self.doctor} - {self.get_day_of_week_display()} ({self.start_time} - {self.end_time})"

class Patient(models.Model):
    """Модель пациента поликлиники"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='patient_profile')
    last_name = models.CharField(_('Фамилия'), max_length=100)
    first_name = models.CharField(_('Имя'), max_length=100)
    middle_name = models.CharField(_('Отчество'), max_length=100, blank=True, null=True)
    date_of_birth = models.DateField(_('Дата рождения'))
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Номер телефона должен быть в формате: '+999999999'.")
    phone_number = models.CharField(_('Номер телефона'), validators=[phone_regex], max_length=17)
    email = models.EmailField(_('Email'), blank=True, null=True)
    address = models.TextField(_('Адрес'), blank=True, null=True)
    insurance_number = models.CharField(_('Номер медицинского полиса'), max_length=16, unique=True)
    
    class Meta:
        verbose_name = _('Пациент')
        verbose_name_plural = _('Пациенты')
        ordering = ['last_name', 'first_name']
    
    def __str__(self):
        return f"{self.last_name} {self.first_name} {self.middle_name or ''}"
    
    @property
    def full_name(self):
        if self.middle_name:
            return f"{self.last_name} {self.first_name} {self.middle_name}"
        return f"{self.last_name} {self.first_name}"

class Appointment(models.Model):
    """Модель записи на прием"""
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE, related_name='appointments', verbose_name=_('Пациент'))
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments', verbose_name=_('Врач'))
    date = models.DateField(_('Дата приема'))
    time = models.TimeField(_('Время приема'))
    status = models.CharField(_('Статус'), max_length=20, choices=STATUS_CHOICES, default='scheduled')
    reason = models.TextField(_('Причина обращения'), blank=True, null=True)
    notes = models.TextField(_('Комментарии'), blank=True, null=True)
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    
    class Meta:
        verbose_name = _('Запись на прием')
        verbose_name_plural = _('Записи на прием')
        ordering = ['-date', '-time']
        unique_together = ['doctor', 'date', 'time']
    
    def __str__(self):
        return f"{self.patient} - {self.doctor} ({self.date} {self.time})"

class MedicalRecord(models.Model):
    """Модель медицинской записи"""
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='medical_record', verbose_name=_('Прием'))
    diagnosis = models.TextField(_('Диагноз'))
    treatment = models.TextField(_('Назначенное лечение'))
    recommendations = models.TextField(_('Рекомендации'))
    created_at = models.DateTimeField(_('Дата создания'), auto_now_add=True)
    updated_at = models.DateTimeField(_('Дата обновления'), auto_now=True)
    
    class Meta:
        verbose_name = _('Медицинская запись')
        verbose_name_plural = _('Медицинские записи')
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Запись для {self.appointment}"

class UserProfile(models.Model):
    """Расширение модели пользователя для хранения роли"""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    ROLE_CHOICES = (
        ('admin', 'Администратор'),
        ('patient', 'Пациент'),
        ('doctor', 'Врач'),
    )
    role = models.CharField(_('Роль'), max_length=20, choices=ROLE_CHOICES, default='patient')
    
    class Meta:
        verbose_name = _('Профиль пользователя')
        verbose_name_plural = _('Профили пользователей')
    
    def __str__(self):
        return f"{self.user.username} - {self.get_role_display()}"
