import random
from datetime import time, timedelta, date
from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from medical.models import Department, Doctor, Schedule, UserProfile

class Command(BaseCommand):
    help = 'Populate database with initial data'

    def handle(self, *args, **kwargs):
        self.stdout.write('Populating database...')
        
        # Create departments
        departments = [
            {
                'name': 'Терапевтическое отделение',
                'description': 'Отделение занимается диагностикой и лечением заболеваний внутренних органов. Врачи-терапевты проводят первичный осмотр пациентов и направляют к узким специалистам при необходимости.',
                'phone': '+7 (123) 456-78-01',
                'email': 'therapy@clinic.ru',
                'floor': 1,
                'room_number': '101-110',
            },
            {
                'name': 'Кардиологическое отделение',
                'description': 'Отделение специализируется на диагностике и лечении заболеваний сердечно-сосудистой системы. Оснащено современным оборудованием для проведения ЭКГ, эхокардиографии и других исследований.',
                'phone': '+7 (123) 456-78-02',
                'email': 'cardio@clinic.ru',
                'floor': 2,
                'room_number': '201-210',
            },
            {
                'name': 'Неврологическое отделение',
                'description': 'Отделение занимается диагностикой и лечением заболеваний нервной системы. Врачи-неврологи проводят консультации и назначают необходимое лечение.',
                'phone': '+7 (123) 456-78-03',
                'email': 'neuro@clinic.ru',
                'floor': 2,
                'room_number': '211-220',
            },
            {
                'name': 'Хирургическое отделение',
                'description': 'Отделение специализируется на хирургическом лечении различных заболеваний. Проводятся как плановые, так и экстренные операции.',
                'phone': '+7 (123) 456-78-04',
                'email': 'surgery@clinic.ru',
                'floor': 3,
                'room_number': '301-310',
            },
            {
                'name': 'Педиатрическое отделение',
                'description': 'Отделение занимается диагностикой и лечением детских заболеваний. Врачи-педиатры проводят консультации и профилактические осмотры детей.',
                'phone': '+7 (123) 456-78-05',
                'email': 'pediatrics@clinic.ru',
                'floor': 1,
                'room_number': '111-120',
            },
            {
                'name': 'Венерологическое отделение',
                'description': 'Отделение специализируется на диагностике, лечении и профилактике заболеваний, передающихся половым путем. Врачи-венерологи проводят консультации и назначают необходимое лечение.',
                'phone': '+7 (123) 456-78-06',
                'email': 'venerology@clinic.ru',
                'floor': 3,
                'room_number': '311-320',
            },
        ]
        
        created_departments = []
        for dept_data in departments:
            department, created = Department.objects.get_or_create(
                name=dept_data['name'],
                defaults=dept_data
            )
            created_departments.append(department)
            action = 'Created' if created else 'Already exists'
            self.stdout.write(f'{action}: {department.name}')
        
        # Create doctors
        doctors_data = [
            # Терапевты
            {
                'last_name': 'Быков',
                'first_name': 'Андрей',
                'middle_name': 'Евгеньевич',
                'specialization': 'Терапевт',
                'experience': 15,
                'department': created_departments[0],
                'bio': 'Опытный врач-терапевт с 15-летним стажем работы. Специализируется на диагностике и лечении заболеваний внутренних органов.',
                'education': 'Московский государственный медицинский университет им. И.М. Сеченова, 2005 г.',
            },
            {
                'last_name': 'Новиков',
                'first_name': 'Андрей',
                'middle_name': 'Михайлович',
                'specialization': 'Терапевт',
                'experience': 5,
                'department': created_departments[0],
                'bio': 'Молодой и перспективный врач-терапевт. Специализируется на профилактической медицине.',
                'education': 'Московский государственный медицинский университет им. И.М. Сеченова, 2015 г.',
            },
            {
                'last_name': 'Соколова',
                'first_name': 'Анна',
                'middle_name': 'Дмитриевна',
                'specialization': 'Терапевт',
                'experience': 12,
                'department': created_departments[0],
                'bio': 'Врач-терапевт высшей категории. Специализируется на лечении заболеваний дыхательной системы.',
                'education': 'Российский национальный исследовательский медицинский университет им. Н.И. Пирогова, 2008 г.',
            },
            
            # Кардиологи
            {
                'last_name': 'Петрова',
                'first_name': 'Мария',
                'middle_name': 'Александровна',
                'specialization': 'Кардиолог',
                'experience': 10,
                'department': created_departments[1],
                'bio': 'Врач-кардиолог высшей категории. Специализируется на диагностике и лечении заболеваний сердечно-сосудистой системы.',
                'education': 'Российский национальный исследовательский медицинский университет им. Н.И. Пирогова, 2010 г.',
            },
            {
                'last_name': 'Морозова',
                'first_name': 'Ольга',
                'middle_name': 'Игоревна',
                'specialization': 'Кардиолог',
                'experience': 7,
                'department': created_departments[1],
                'bio': 'Врач-кардиолог с 7-летним опытом работы. Специализируется на диагностике и лечении аритмий.',
                'education': 'Российский национальный исследовательский медицинский университет им. Н.И. Пирогова, 2013 г.',
            },
            {
                'last_name': 'Кузнецов',
                'first_name': 'Виктор',
                'middle_name': 'Андреевич',
                'specialization': 'Кардиолог',
                'experience': 20,
                'department': created_departments[1],
                'bio': 'Врач-кардиолог с 20-летним стажем работы. Специализируется на лечении ишемической болезни сердца.',
                'education': 'Московский государственный медицинский университет им. И.М. Сеченова, 2000 г.',
            },
            
            # Неврологи
            {
                'last_name': 'Сидоров',
                'first_name': 'Алексей',
                'middle_name': 'Петрович',
                'specialization': 'Невролог',
                'experience': 12,
                'department': created_departments[2],
                'bio': 'Врач-невролог с 12-летним опытом работы. Специализируется на диагностике и лечении заболеваний нервной системы.',
                'education': 'Санкт-Петербургский государственный медицинский университет им. акад. И.П. Павлова, 2008 г.',
            },
            {
                'last_name': 'Волков',
                'first_name': 'Сергей',
                'middle_name': 'Александрович',
                'specialization': 'Невролог',
                'experience': 9,
                'department': created_departments[2],
                'bio': 'Врач-невролог с 9-летним опытом работы. Специализируется на лечении головных болей и мигреней.',
                'education': 'Московский государственный медицинский университет им. И.М. Сеченова, 2011 г.',
            },
            {
                'last_name': 'Лебедева',
                'first_name': 'Екатерина',
                'middle_name': 'Сергеевна',
                'specialization': 'Невролог',
                'experience': 15,
                'department': created_departments[2],
                'bio': 'Врач-невролог высшей категории. Специализируется на лечении нейродегенеративных заболеваний.',
                'education': 'Российский национальный исследовательский медицинский университет им. Н.И. Пирогова, 2005 г.',
            },
            
            # Хирурги
            {
                'last_name': 'Козлов',
                'first_name': 'Дмитрий',
                'middle_name': 'Сергеевич',
                'specialization': 'Хирург',
                'experience': 18,
                'department': created_departments[3],
                'bio': 'Врач-хирург высшей категории с 18-летним стажем работы. Специализируется на общей хирургии.',
                'education': 'Московский государственный медицинский университет им. И.М. Сеченова, 2002 г.',
            },
            {
                'last_name': 'Григорьев',
                'first_name': 'Николай',
                'middle_name': 'Иванович',
                'specialization': 'Хирург',
                'experience': 22,
                'department': created_departments[3],
                'bio': 'Врач-хирург высшей категории. Специализируется на лапароскопических операциях.',
                'education': 'Санкт-Петербургский государственный медицинский университет им. акад. И.П. Павлова, 1998 г.',
            },
            {
                'last_name': 'Федорова',
                'first_name': 'Анастасия',
                'middle_name': 'Владимировна',
                'specialization': 'Хирург',
                'experience': 8,
                'department': created_departments[3],
                'bio': 'Врач-хирург с 8-летним опытом работы. Специализируется на малоинвазивной хирургии.',
                'education': 'Российский национальный исследовательский медицинский университет им. Н.И. Пирогова, 2012 г.',
            },
            
            # Педиатры
            {
                'last_name': 'Смирнова',
                'first_name': 'Елена',
                'middle_name': 'Владимировна',
                'specialization': 'Педиатр',
                'experience': 8,
                'department': created_departments[4],
                'bio': 'Врач-педиатр с 8-летним опытом работы. Специализируется на диагностике и лечении детских заболеваний.',
                'education': 'Российский национальный исследовательский медицинский университет им. Н.И. Пирогова, 2012 г.',
            },
            {
                'last_name': 'Попов',
                'first_name': 'Михаил',
                'middle_name': 'Алексеевич',
                'specialization': 'Педиатр',
                'experience': 14,
                'department': created_departments[4],
                'bio': 'Врач-педиатр высшей категории. Специализируется на лечении детских инфекционных заболеваний.',
                'education': 'Московский государственный медицинский университет им. И.М. Сеченова, 2006 г.',
            },
            {
                'last_name': 'Никитина',
                'first_name': 'Татьяна',
                'middle_name': 'Игоревна',
                'specialization': 'Педиатр',
                'experience': 6,
                'department': created_departments[4],
                'bio': 'Врач-педиатр с 6-летним опытом работы. Специализируется на профилактической педиатрии и вакцинации.',
                'education': 'Российский национальный исследовательский медицинский университет им. Н.И. Пирогова, 2014 г.',
            },
            
            # Психотерапевты
            {
                'last_name': 'Белов',
                'first_name': 'Артем',
                'middle_name': 'Валерьевич',
                'specialization': 'Психотерапевт',
                'experience': 16,
                'department': created_departments[2],
                'bio': 'Врач-психотерапевт высшей категории. Специализируется на когнитивно-поведенческой терапии.',
                'education': 'Московский государственный медицинский университет им. И.М. Сеченова, 2004 г.',
            },
            {
                'last_name': 'Романова',
                'first_name': 'Ирина',
                'middle_name': 'Павловна',
                'specialization': 'Психотерапевт',
                'experience': 12,
                'department': created_departments[2],
                'bio': 'Врач-психотерапевт с 12-летним опытом работы. Специализируется на семейной психотерапии.',
                'education': 'Российский национальный исследовательский медицинский университет им. Н.И. Пирогова, 2008 г.',
            },
            {
                'last_name': 'Макаров',
                'first_name': 'Денис',
                'middle_name': 'Олегович',
                'specialization': 'Психотерапевт',
                'experience': 9,
                'department': created_departments[2],
                'bio': 'Врач-психотерапевт с 9-летним опытом работы. Специализируется на лечении тревожных расстройств и депрессии.',
                'education': 'Санкт-Петербургский государственный медицинский университет им. акад. И.П. Павлова, 2011 г.',
            },
            {
                'last_name': 'Соловьева',
                'first_name': 'Наталья',
                'middle_name': 'Андреевна',
                'specialization': 'Психотерапевт',
                'experience': 7,
                'department': created_departments[2],
                'bio': 'Врач-психотерапевт с 7-летним опытом работы. Специализируется на психосоматических расстройствах.',
                'education': 'Московский государственный медицинский университет им. И.М. Сеченова, 2013 г.',
            },
            
            # Инфекционисты
            {
                'last_name': 'Орлов',
                'first_name': 'Владимир',
                'middle_name': 'Петрович',
                'specialization': 'Инфекционист',
                'experience': 20,
                'department': created_departments[0],
                'bio': 'Врач-инфекционист высшей категории с 20-летним стажем работы. Специализируется на лечении вирусных гепатитов.',
                'education': 'Московский государственный медицинский университет им. И.М. Сеченова, 2000 г.',
            },
            {
                'last_name': 'Антонова',
                'first_name': 'Светлана',
                'middle_name': 'Викторовна',
                'specialization': 'Инфекционист',
                'experience': 15,
                'department': created_departments[0],
                'bio': 'Врач-инфекционист с 15-летним опытом работы. Специализируется на лечении кишечных инфекций.',
                'education': 'Российский национальный исследовательский медицинский университет им. Н.И. Пирогова, 2005 г.',
            },
            {
                'last_name': 'Захаров',
                'first_name': 'Игорь',
                'middle_name': 'Сергеевич',
                'specialization': 'Инфекционист',
                'experience': 10,
                'department': created_departments[0],
                'bio': 'Врач-инфекционист с 10-летним опытом работы. Специализируется на лечении респираторных инфекций.',
                'education': 'Санкт-Петербургский государственный медицинский университет им. акад. И.П. Павлова, 2010 г.',
            },
            
            # Стоматологи
            {
                'last_name': 'Королев',
                'first_name': 'Максим',
                'middle_name': 'Дмитриевич',
                'specialization': 'Стоматолог',
                'experience': 18,
                'department': created_departments[3],
                'bio': 'Врач-стоматолог высшей категории. Специализируется на эстетической стоматологии и протезировании.',
                'education': 'Московский государственный медико-стоматологический университет им. А.И. Евдокимова, 2002 г.',
            },
            {
                'last_name': 'Медведева',
                'first_name': 'Юлия',
                'middle_name': 'Александровна',
                'specialization': 'Стоматолог',
                'experience': 12,
                'department': created_departments[3],
                'bio': 'Врач-стоматолог с 12-летним опытом работы. Специализируется на лечении кариеса и его осложнений.',
                'education': 'Московский государственный медико-стоматологический университет им. А.И. Евдокимова, 2008 г.',
            },
            {
                'last_name': 'Тихонов',
                'first_name': 'Алексей',
                'middle_name': 'Владимирович',
                'specialization': 'Стоматолог',
                'experience': 9,
                'department': created_departments[3],
                'bio': 'Врач-стоматолог с 9-летним опытом работы. Специализируется на хирургической стоматологии и имплантации.',
                'education': 'Московский государственный медико-стоматологический университет им. А.И. Евдокимова, 2011 г.',
            },
            {
                'last_name': 'Калинина',
                'first_name': 'Марина',
                'middle_name': 'Евгеньевна',
                'specialization': 'Стоматолог',
                'experience': 7,
                'department': created_departments[3],
                'bio': 'Врач-стоматолог с 7-летним опытом работы. Специализируется на детской стоматологии.',
                'education': 'Московский государственный медико-стоматологический университет им. А.И. Евдокимова, 2013 г.',
            },
            {
                'last_name': 'Филиппов',
                'first_name': 'Роман',
                'middle_name': 'Игоревич',
                'specialization': 'Стоматолог',
                'experience': 5,
                'department': created_departments[3],
                'bio': 'Врач-стоматолог с 5-летним опытом работы. Специализируется на эндодонтии и микроскопической стоматологии.',
                'education': 'Московский государственный медико-стоматологический университет им. А.И. Евдокимова, 2015 г.',
            },
            
            # Венерологи
            {
                'last_name': 'Купитман',
                'first_name': 'Иван',
                'middle_name': 'Натанович',
                'specialization': 'Венеролог',
                'experience': 15,
                'department': created_departments[5],
                'bio': 'Врач-венеролог высшей категории с 15-летним стажем работы. Специализируется на диагностике и лечении заболеваний, передающихся половым путем.',
                'education': 'Российский национальный исследовательский медицинский университет им. Н.И. Пирогова, 2005 г.',
            },
            {
                'last_name': 'Ковалева',
                'first_name': 'Анна',
                'middle_name': 'Сергеевна',
                'specialization': 'Венеролог',
                'experience': 10,
                'department': created_departments[5],
                'bio': 'Врач-венеролог с 10-летним опытом работы. Специализируется на лечении урогенитальных инфекций и воспалительных заболеваний.',
                'education': 'Московский государственный медицинский университет им. И.М. Сеченова, 2010 г.',
            },
            {
                'last_name': 'Игнатьев',
                'first_name': 'Павел',
                'middle_name': 'Андреевич',
                'specialization': 'Венеролог',
                'experience': 8,
                'department': created_departments[5],
                'bio': 'Врач-венеролог с 8-летним опытом работы. Специализируется на профилактике и лечении ИППП, а также на дерматовенерологии.',
                'education': 'Санкт-Петербургский государственный медицинский университет им. акад. И.П. Павлова, 2012 г.',
            },
        ]
        
        created_doctors = []
        for doctor_data in doctors_data:
            doctor, created = Doctor.objects.get_or_create(
                last_name=doctor_data['last_name'],
                first_name=doctor_data['first_name'],
                middle_name=doctor_data['middle_name'],
                defaults=doctor_data
            )
            created_doctors.append(doctor)
            action = 'Created' if created else 'Already exists'
            self.stdout.write(f'{action}: {doctor.full_name} - {doctor.specialization}')
            
            # Create user for doctor if it doesn't exist
            username = f"{doctor.last_name.lower()}.{doctor.first_name.lower()}"
            if not User.objects.filter(username=username).exists():
                user = User.objects.create_user(
                    username=username,
                    email=f"{username}@clinic.ru",
                    password="password123",
                    first_name=doctor.first_name,
                    last_name=doctor.last_name
                )
                doctor.user = user
                doctor.save()
                
                # Create user profile
                UserProfile.objects.get_or_create(
                    user=user,
                    defaults={'role': 'doctor'}
                )
                self.stdout.write(f'Created user for doctor: {username}')
        
        # Create schedules for doctors
        for doctor in created_doctors:
            for day in range(1, 8):  # 1-7 (Monday to Sunday)
                # Weekend on Saturday and Sunday
                is_working_day = day < 6
                
                # Random start and end times for working days
                if is_working_day:
                    start_hour = random.choice([8, 9])
                    end_hour = random.choice([17, 18])
                    start_time_obj = time(start_hour, 0)
                    end_time_obj = time(end_hour, 0)
                else:
                    start_time_obj = time(0, 0)
                    end_time_obj = time(0, 0)
                
                schedule, created = Schedule.objects.get_or_create(
                    doctor=doctor,
                    day_of_week=day,
                    defaults={
                        'start_time': start_time_obj,
                        'end_time': end_time_obj,
                        'is_working_day': is_working_day
                    }
                )
                
                if created:
                    self.stdout.write(f'Created schedule for {doctor.full_name} on {schedule.get_day_of_week_display()}')
        
        # Create admin user profile if it doesn't exist
        admin_user = User.objects.filter(is_superuser=True).first()
        if admin_user:
            UserProfile.objects.get_or_create(
                user=admin_user,
                defaults={'role': 'admin'}
            )
            self.stdout.write(f'Created admin profile for user: {admin_user.username}')
        
        self.stdout.write(self.style.SUCCESS('Database populated successfully!'))