from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _
from .models import Patient, Appointment, Doctor, Department, UserProfile, MedicalRecord

class UserLoginForm(AuthenticationForm):
    """Форма авторизации пользователя"""
    username = forms.CharField(
        label=_('Имя пользователя'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Имя пользователя')})
    )
    password = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Пароль')})
    )

class UserRegisterForm(UserCreationForm):
    """Форма регистрации пользователя"""
    username = forms.CharField(
        label=_('Имя пользователя'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Имя пользователя')})
    )
    email = forms.EmailField(
        label=_('Email'),
        widget=forms.EmailInput(attrs={'class': 'form-control', 'placeholder': _('Email')})
    )
    last_name = forms.CharField(
        label=_('Фамилия'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Фамилия')})
    )
    first_name = forms.CharField(
        label=_('Имя'),
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Имя')})
    )
    middle_name = forms.CharField(
        label=_('Отчество'),
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': _('Отчество')})
    )
    password1 = forms.CharField(
        label=_('Пароль'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Пароль')})
    )
    password2 = forms.CharField(
        label=_('Подтверждение пароля'),
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': _('Подтверждение пароля')})
    )
    
    class Meta:
        model = User
        fields = ['username', 'email', 'last_name', 'first_name', 'password1', 'password2']

class PatientProfileForm(forms.ModelForm):
    """Форма профиля пациента"""
    class Meta:
        model = Patient
        fields = [
            'last_name', 'first_name', 'middle_name', 'date_of_birth',
            'phone_number', 'email', 'address', 'insurance_number'
        ]
        widgets = {
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'middle_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'insurance_number': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Если это существующий пациент и у него есть дата рождения
        if self.instance and self.instance.pk and self.instance.date_of_birth:
            # Форматируем дату в строку в формате YYYY-MM-DD для HTML input type="date"
            self.initial['date_of_birth'] = self.instance.date_of_birth.strftime('%Y-%m-%d')

class AppointmentForm(forms.ModelForm):
    """Форма записи на прием"""
    class Meta:
        model = Appointment
        fields = ['date', 'time', 'reason']  # Убрали doctor из полей формы
        widgets = {
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        # Получаем doctor из initial, если он есть
        self.doctor = None
        if 'initial' in kwargs and 'doctor' in kwargs['initial']:
            self.doctor = kwargs['initial']['doctor']
            
        super().__init__(*args, **kwargs)
    
    def clean(self):
        cleaned_data = super().clean()
        date = cleaned_data.get('date')
        time = cleaned_data.get('time')
        
        # Проверяем, что все необходимые поля заполнены
        if self.doctor and date and time:
            # Проверяем, нет ли уже записи на это время
            if Appointment.objects.filter(
                doctor=self.doctor,
                date=date,
                time=time,
                status__in=['scheduled', 'completed']
            ).exists():
                self.add_error('time', _('Выбранное время уже занято. Пожалуйста, выберите другое время.'))
        
        return cleaned_data

class AppointmentAdminForm(forms.ModelForm):
    """Форма записи на прием для администратора"""
    class Meta:
        model = Appointment
        fields = ['patient', 'doctor', 'date', 'time', 'status', 'reason', 'notes']
        widgets = {
            'patient': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'reason': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class MedicalRecordForm(forms.ModelForm):
    """Форма медицинской записи"""
    class Meta:
        model = MedicalRecord
        fields = ['diagnosis', 'treatment', 'recommendations']
        widgets = {
            'diagnosis': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'treatment': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'recommendations': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class DoctorFilterForm(forms.Form):
    """Форма фильтрации врачей"""
    department = forms.ModelChoiceField(
        queryset=Department.objects.all(),
        required=False,
        empty_label=_("Все отделения"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    specialization = forms.ChoiceField(
        choices=[('', _('Все специализации'))],
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Динамически получаем все специализации из базы данных без дубликатов
        specializations = Doctor.objects.values_list('specialization', flat=True).distinct().order_by('specialization')
        # Преобразуем QuerySet в список и удаляем дубликаты
        unique_specializations = list(dict.fromkeys(specializations))
        self.fields['specialization'].choices += [(spec, spec) for spec in unique_specializations]