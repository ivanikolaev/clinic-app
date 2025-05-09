from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy

from .models import (
    Department, Doctor, Schedule, Patient, 
    Appointment, MedicalRecord, UserProfile
)
from .forms import (
    UserRegisterForm, UserLoginForm, PatientProfileForm,
    AppointmentForm, AppointmentAdminForm, MedicalRecordForm,
    DoctorFilterForm
)

def home(request):
    """Главная страница"""
    departments = Department.objects.all()[:4]
    doctors = Doctor.objects.all().order_by('?')[:8]  # Случайные 8 врачей
    
    context = {
        'title': _('Главная'),
        'departments': departments,
        'doctors': doctors,
    }
    return render(request, 'medical/home.html', context)

def about(request):
    """Страница о поликлинике"""
    context = {
        'title': _('О поликлинике'),
    }
    return render(request, 'medical/about.html', context)

def contact(request):
    """Страница контактов"""
    context = {
        'title': _('Контакты'),
    }
    return render(request, 'medical/contact.html', context)

def register(request):
    """Регистрация пользователя"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            # Сохраняем данные пользователя
            user = form.save()
            
            # Создаем профиль пользователя с ролью "пациент"
            UserProfile.objects.create(user=user, role='patient')
            
            # Сохраняем middle_name в сессии для использования при создании профиля пациента
            request.session['middle_name'] = form.cleaned_data.get('middle_name', '')
            
            login(request, user)
            messages.success(request, _('Вы успешно зарегистрировались! Теперь заполните свой профиль.'))
            return redirect('patient_profile_create')
        else:
            messages.error(request, _('Ошибка регистрации. Пожалуйста, проверьте данные.'))
    else:
        form = UserRegisterForm()
    
    context = {
        'title': _('Регистрация'),
        'form': form,
    }
    return render(request, 'medical/register.html', context)

def user_login(request):
    """Авторизация пользователя"""
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, _('Вы успешно вошли в систему!'))
            return redirect('home')
        else:
            messages.error(request, _('Ошибка входа. Пожалуйста, проверьте данные.'))
    else:
        form = UserLoginForm()
    
    context = {
        'title': _('Вход'),
        'form': form,
    }
    return render(request, 'medical/login.html', context)

@login_required
def user_logout(request):
    """Выход пользователя"""
    logout(request)
    messages.success(request, _('Вы вышли из системы.'))
    return redirect('home')

@login_required
def patient_profile_create(request):
    """Создание профиля пациента"""
    # Проверяем, есть ли уже профиль у пользователя
    try:
        patient = Patient.objects.get(user=request.user)
        messages.info(request, _('У вас уже есть профиль.'))
        return redirect('patient_profile')
    except Patient.DoesNotExist:
        pass
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)
            patient.user = request.user
            patient.save()
            
            # Удаляем middle_name из сессии после использования
            if 'middle_name' in request.session:
                del request.session['middle_name']
                
            messages.success(request, _('Профиль успешно создан!'))
            return redirect('patient_profile')
        else:
            messages.error(request, _('Ошибка создания профиля. Пожалуйста, проверьте данные.'))
    else:
        # Предзаполняем форму данными пользователя
        initial_data = {
            'first_name': request.user.first_name,
            'last_name': request.user.last_name,
            'email': request.user.email,
        }
        
        # Добавляем отчество из сессии, если оно есть
        if 'middle_name' in request.session:
            initial_data['middle_name'] = request.session['middle_name']
            
        form = PatientProfileForm(initial=initial_data)
    
    context = {
        'title': _('Создание профиля'),
        'form': form,
    }
    return render(request, 'medical/patient_profile_form.html', context)

@login_required
def patient_profile(request):
    """Просмотр профиля пациента"""
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.warning(request, _('Сначала заполните свой профиль.'))
        return redirect('patient_profile_create')
    
    context = {
        'title': _('Мой профиль'),
        'patient': patient,
    }
    return render(request, 'medical/patient_profile.html', context)

@login_required
def patient_profile_update(request):
    """Обновление профиля пациента"""
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.warning(request, _('Сначала заполните свой профиль.'))
        return redirect('patient_profile_create')
    
    if request.method == 'POST':
        form = PatientProfileForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            messages.success(request, _('Профиль успешно обновлен!'))
            return redirect('patient_profile')
        else:
            messages.error(request, _('Ошибка обновления профиля. Пожалуйста, проверьте данные.'))
    else:
        # Создаем форму с существующими данными пациента
        form = PatientProfileForm(instance=patient)
        
        # Если дата рождения существует, форматируем ее в строку в формате YYYY-MM-DD для HTML input type="date"
        if patient.date_of_birth:
            form.initial['date_of_birth'] = patient.date_of_birth.strftime('%Y-%m-%d')
    
    context = {
        'title': _('Редактирование профиля'),
        'form': form,
    }
    return render(request, 'medical/patient_profile_form.html', context)

class DepartmentListView(ListView):
    """Список отделений"""
    model = Department
    template_name = 'medical/department_list.html'
    context_object_name = 'departments'
    paginate_by = 10
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Отделения')
        return context

class DepartmentDetailView(DetailView):
    """Детальная информация об отделении"""
    model = Department
    template_name = 'medical/department_detail.html'
    context_object_name = 'department'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.name
        context['doctors'] = self.object.doctors.all()
        return context

def doctor_list(request):
    """Список врачей с фильтрацией"""
    doctors = Doctor.objects.all()
    
    # Фильтрация
    form = DoctorFilterForm(request.GET)
    if form.is_valid():
        department = form.cleaned_data.get('department')
        specialization = form.cleaned_data.get('specialization')
        
        if department:
            doctors = doctors.filter(department=department)
        if specialization:
            doctors = doctors.filter(specialization=specialization)
    
    context = {
        'title': _('Врачи'),
        'doctors': doctors,
        'form': form,
    }
    return render(request, 'medical/doctor_list.html', context)

class DoctorDetailView(DetailView):
    """Детальная информация о враче"""
    model = Doctor
    template_name = 'medical/doctor_detail.html'
    context_object_name = 'doctor'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.object.full_name
        context['schedules'] = self.object.schedules.all().order_by('day_of_week')
        
        # Если пользователь авторизован и является пациентом, показываем форму записи
        if self.request.user.is_authenticated:
            try:
                patient = Patient.objects.get(user=self.request.user)
                context['appointment_form'] = AppointmentForm(initial={'doctor': self.object})
                context['patient'] = patient
            except Patient.DoesNotExist:
                pass
        
        return context

@login_required
def appointment_create(request, doctor_id):
    """Создание записи на прием"""
    doctor = get_object_or_404(Doctor, id=doctor_id)
    
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.warning(request, _('Сначала заполните свой профиль.'))
        return redirect('patient_profile_create')
    
    if request.method == 'POST':
        # Создаем форму с предварительно заполненным полем doctor
        form = AppointmentForm(request.POST, initial={'doctor': doctor})
        # Явно устанавливаем doctor в форме
        form.doctor = doctor
        
        # Выводим данные формы для отладки
        print(f"Form data: {request.POST}")
        
        if form.is_valid():
            try:
                # Создаем запись, но не сохраняем пока
                appointment = form.save(commit=False)
                appointment.patient = patient
                appointment.doctor = doctor  # Явно устанавливаем врача
                appointment.status = 'scheduled'
                
                # Выводим данные записи для отладки
                print(f"Appointment data: date={appointment.date}, time={appointment.time}, doctor={doctor.id}, patient={patient.id}")
                
                # Сохраняем запись
                appointment.save()
                messages.success(request, _('Вы успешно записались на прием!'))
                return redirect('appointment_list')
            except Exception as e:
                # Выводим ошибку для отладки
                print(f"Error saving appointment: {str(e)}")
                messages.error(request, _('Произошла ошибка при сохранении записи: {0}').format(str(e)))
        else:
            # Выводим ошибки формы для отладки
            print(f"Form errors: {form.errors}")
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field}: {error}")
    else:
        # Создаем форму с предварительно заполненным полем doctor
        form = AppointmentForm(initial={'doctor': doctor})
        # Явно устанавливаем doctor в форме
        form.doctor = doctor
    
    context = {
        'title': _('Запись на прием'),
        'form': form,
        'doctor': doctor,
    }
    return render(request, 'medical/appointment_form.html', context)

@login_required
def appointment_list(request):
    """Список записей на прием пациента"""
    try:
        patient = Patient.objects.get(user=request.user)
    except Patient.DoesNotExist:
        messages.warning(request, _('Сначала заполните свой профиль.'))
        return redirect('patient_profile_create')
    
    # Получаем все записи пациента
    appointments = Appointment.objects.filter(patient=patient).order_by('-date', '-time')
    
    # Фильтрация по статусу
    status = request.GET.get('status')
    if status:
        appointments = appointments.filter(status=status)
    
    # Пагинация
    paginator = Paginator(appointments, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'title': _('Мои записи'),
        'page_obj': page_obj,
        'status': status,
    }
    return render(request, 'medical/appointment_list.html', context)

@login_required
def appointment_detail(request, pk):
    """Детальная информация о записи на прием"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Проверяем, что пользователь имеет доступ к этой записи
    if request.user.profile.role == 'patient' and appointment.patient.user != request.user:
        messages.error(request, _('У вас нет доступа к этой записи.'))
        return redirect('appointment_list')
    
    context = {
        'title': _('Информация о записи'),
        'appointment': appointment,
    }
    
    # Если есть медицинская запись, добавляем ее в контекст
    try:
        medical_record = appointment.medical_record
        context['medical_record'] = medical_record
    except MedicalRecord.DoesNotExist:
        pass
    
    return render(request, 'medical/appointment_detail.html', context)

@login_required
def appointment_cancel(request, pk):
    """Отмена записи на прием"""
    appointment = get_object_or_404(Appointment, pk=pk)
    
    # Проверяем, что пользователь имеет доступ к этой записи
    if request.user.profile.role == 'patient' and appointment.patient.user != request.user:
        messages.error(request, _('У вас нет доступа к этой записи.'))
        return redirect('appointment_list')
    
    # Проверяем, что запись еще не завершена
    if appointment.status in ['completed', 'cancelled', 'no_show']:
        messages.error(request, _('Невозможно отменить запись с текущим статусом.'))
        return redirect('appointment_detail', pk=appointment.pk)
    
    if request.method == 'POST':
        appointment.status = 'cancelled'
        appointment.save()
        messages.success(request, _('Запись успешно отменена.'))
        return redirect('appointment_list')
    
    context = {
        'title': _('Отмена записи'),
        'appointment': appointment,
    }
    return render(request, 'medical/appointment_cancel.html', context)

# Административные представления

class AdminRequiredMixin(UserPassesTestMixin):
    """Миксин для проверки, что пользователь является администратором"""
    def test_func(self):
        return self.request.user.is_authenticated and (
            self.request.user.is_staff or 
            hasattr(self.request.user, 'profile') and self.request.user.profile.role == 'admin'
        )

class AdminDashboardView(AdminRequiredMixin, ListView):
    """Административная панель"""
    model = Appointment
    template_name = 'medical/admin/dashboard.html'
    context_object_name = 'appointments'
    paginate_by = 10
    
    def get_queryset(self):
        # Получаем записи на сегодня и будущие даты
        from datetime import datetime, time
        
        # Получаем параметры из запроса или используем текущую дату
        date_from = self.request.GET.get('date_from')
        time_from = self.request.GET.get('time_from')
        
        # Если параметры не указаны, используем текущую дату и время
        if not date_from:
            date_from = datetime.now().date()
        
        if not time_from:
            time_from = datetime.now().time()
        
        # Фильтруем записи
        queryset = Appointment.objects.all()
        
        # Применяем фильтр по дате и времени, если они указаны
        if date_from:
            queryset = queryset.filter(
                Q(date__gt=date_from) |
                Q(date=date_from, time__gte=time_from)
            )
        
        # Сортируем по дате и времени
        queryset = queryset.order_by('date', 'time')
        
        # Фильтрация по статусу
        status = self.request.GET.get('status')
        if status:
            queryset = queryset.filter(status=status)
        
        # Фильтрация по врачу
        doctor_id = self.request.GET.get('doctor')
        if doctor_id:
            queryset = queryset.filter(doctor_id=doctor_id)
        
        return queryset
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Панель администратора')
        context['doctors'] = Doctor.objects.all()
        context['total_patients'] = Patient.objects.count()
        context['total_doctors'] = Doctor.objects.count()
        context['total_appointments'] = Appointment.objects.count()
        context['scheduled_appointments'] = Appointment.objects.filter(status='scheduled').count()
        return context

class AdminAppointmentUpdateView(AdminRequiredMixin, UpdateView):
    """Обновление записи на прием администратором"""
    model = Appointment
    form_class = AppointmentAdminForm
    template_name = 'medical/admin/appointment_form.html'
    success_url = reverse_lazy('admin_dashboard')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = _('Редактирование записи')
        
        # Если запись завершена, показываем форму медицинской записи
        if self.object.status == 'completed':
            try:
                medical_record = self.object.medical_record
                context['medical_record_form'] = MedicalRecordForm(instance=medical_record)
            except MedicalRecord.DoesNotExist:
                context['medical_record_form'] = MedicalRecordForm()
        
        return context
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, _('Запись успешно обновлена!'))
        
        # Если запись завершена и есть форма медицинской записи, сохраняем ее
        if self.object.status == 'completed' and 'medical_record_form' in self.request.POST:
            try:
                medical_record = self.object.medical_record
            except MedicalRecord.DoesNotExist:
                medical_record = MedicalRecord(appointment=self.object)
            
            medical_record_form = MedicalRecordForm(self.request.POST, instance=medical_record)
            if medical_record_form.is_valid():
                medical_record_form.save()
                messages.success(self.request, _('Медицинская запись успешно сохранена!'))
        
        return response

# API для получения свободных слотов времени
@login_required
def get_available_slots(request):
    """API для получения свободных слотов времени для записи"""
    doctor_id = request.GET.get('doctor_id')
    date = request.GET.get('date')
    
    if not doctor_id or not date:
        return JsonResponse({'error': _('Не указан врач или дата')}, status=400)
    
    try:
        doctor = Doctor.objects.get(id=doctor_id)
    except Doctor.DoesNotExist:
        return JsonResponse({'error': _('Врач не найден')}, status=404)
    
    # Получаем день недели для указанной даты
    from datetime import datetime
    date_obj = datetime.strptime(date, '%Y-%m-%d')
    day_of_week = date_obj.isoweekday()  # 1 - понедельник, 7 - воскресенье
    
    # Получаем расписание врача на этот день недели
    try:
        schedule = Schedule.objects.get(doctor=doctor, day_of_week=day_of_week)
    except Schedule.DoesNotExist:
        return JsonResponse({'slots': []})  # В этот день врач не работает
    
    if not schedule.is_working_day:
        return JsonResponse({'slots': []})  # Это нерабочий день
    
    # Генерируем временные слоты с интервалом 30 минут
    from datetime import time, timedelta
    slots = []
    current_time = schedule.start_time
    end_time = schedule.end_time
    
    while current_time < end_time:
        # Проверяем, не занят ли этот слот
        time_str = current_time.strftime('%H:%M:%S')
        is_booked = Appointment.objects.filter(
            doctor=doctor,
            date=date,
            time=time_str,
            status__in=['scheduled', 'completed']
        ).exists()
        
        if not is_booked:
            slots.append(time_str)
        
        # Увеличиваем время на 30 минут
        hour, minute, second = current_time.hour, current_time.minute, current_time.second
        minute += 30
        if minute >= 60:
            hour += 1
            minute -= 60
        current_time = time(hour, minute, second)
    
    return JsonResponse({'slots': slots})
