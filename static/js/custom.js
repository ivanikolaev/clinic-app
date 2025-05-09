// Custom JavaScript for Clinic Application

document.addEventListener('DOMContentLoaded', function() {
    // Auto-hide alerts after 5 seconds
    setTimeout(function() {
        const alerts = document.querySelectorAll('.alert:not(.alert-permanent)');
        alerts.forEach(function(alert) {
            const bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // Initialize tooltips
    const tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
    tooltipTriggerList.map(function(tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl);
    });

    // Initialize popovers
    const popoverTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="popover"]'));
    popoverTriggerList.map(function(popoverTriggerEl) {
        return new bootstrap.Popover(popoverTriggerEl);
    });

    // Doctor filter form submission
    const doctorFilterForm = document.getElementById('doctorFilterForm');
    if (doctorFilterForm) {
        doctorFilterForm.addEventListener('submit', function(e) {
            e.preventDefault();
            const department = document.getElementById('id_department').value;
            const specialization = document.getElementById('id_specialization').value;
            
            let url = `${window.location.pathname}?`;
            if (department) {
                url += `department=${department}&`;
            }
            if (specialization) {
                url += `specialization=${specialization}&`;
            }
            
            window.location.href = url.slice(0, -1); // Remove trailing & or ?
        });
    }

    // Appointment time slot selection
    const timeSlots = document.querySelectorAll('.time-slot');
    if (timeSlots.length > 0) {
        timeSlots.forEach(function(slot) {
            slot.addEventListener('click', function() {
                // Remove selected class from all slots
                timeSlots.forEach(function(s) {
                    s.classList.remove('selected');
                });
                
                // Add selected class to clicked slot
                this.classList.add('selected');
                
                // Update hidden input with selected time
                const timeInput = document.getElementById('id_time');
                if (timeInput) {
                    timeInput.value = this.dataset.time;
                }
                
                // Enable submit button
                const submitBtn = document.getElementById('submitBtn');
                if (submitBtn) {
                    submitBtn.disabled = false;
                }
            });
        });
    }

    // Date picker for appointment
    const datePicker = document.getElementById('id_date');
    if (datePicker) {
        datePicker.addEventListener('change', function() {
            const date = this.value;
            const doctorId = document.getElementById('doctorId').value;
            
            if (date) {
                // Clear previous time selection
                document.getElementById('id_time').value = '';
                document.getElementById('submitBtn').disabled = true;
                
                // Fetch available time slots
                fetch(`/api/available-slots/?doctor_id=${doctorId}&date=${date}`)
                    .then(response => response.json())
                    .then(data => {
                        const timeSlotsContainer = document.getElementById('timeSlots');
                        timeSlotsContainer.innerHTML = '';
                        
                        if (data.slots && data.slots.length > 0) {
                            document.getElementById('timeSlotContainer').style.display = 'block';
                            
                            data.slots.forEach(function(slot) {
                                // Convert time from HH:MM:SS to HH:MM
                                const time = slot.substring(0, 5);
                                
                                const timeSlotHtml = `
                                    <div class="col-md-3 col-6 mb-2">
                                        <div class="card time-slot" data-time="${slot}">
                                            <div class="card-body text-center py-2">
                                                ${time}
                                            </div>
                                        </div>
                                    </div>
                                `;
                                
                                timeSlotsContainer.innerHTML += timeSlotHtml;
                            });
                            
                            // Add event listeners to new time slots
                            const newTimeSlots = document.querySelectorAll('.time-slot');
                            newTimeSlots.forEach(function(slot) {
                                slot.addEventListener('click', function() {
                                    newTimeSlots.forEach(function(s) {
                                        s.classList.remove('selected');
                                    });
                                    
                                    this.classList.add('selected');
                                    
                                    document.getElementById('id_time').value = this.dataset.time;
                                    document.getElementById('submitBtn').disabled = false;
                                });
                            });
                        } else {
                            document.getElementById('timeSlotContainer').style.display = 'block';
                            timeSlotsContainer.innerHTML = `
                                <div class="col-12">
                                    <div class="alert alert-info">
                                        На выбранную дату нет доступных слотов времени. Пожалуйста, выберите другую дату.
                                    </div>
                                </div>
                            `;
                        }
                    })
                    .catch(error => {
                        document.getElementById('timeSlotContainer').style.display = 'block';
                        document.getElementById('timeSlots').innerHTML = `
                            <div class="col-12">
                                <div class="alert alert-danger">
                                    Произошла ошибка при загрузке доступных слотов времени. Пожалуйста, попробуйте еще раз.
                                </div>
                            </div>
                        `;
                    });
            } else {
                document.getElementById('timeSlotContainer').style.display = 'none';
                document.getElementById('timeSlots').innerHTML = '';
                document.getElementById('id_time').value = '';
                document.getElementById('submitBtn').disabled = true;
            }
        });
    }

    // Form validation
    const appointmentForm = document.getElementById('appointmentForm');
    if (appointmentForm) {
        appointmentForm.addEventListener('submit', function(e) {
            if (!document.getElementById('id_date').value || !document.getElementById('id_time').value) {
                e.preventDefault();
                alert('Пожалуйста, выберите дату и время приема.');
            }
        });
    }

    // Show/hide appointment form
    const showAppointmentFormBtn = document.getElementById('showAppointmentForm');
    if (showAppointmentFormBtn) {
        showAppointmentFormBtn.addEventListener('click', function() {
            document.getElementById('appointmentFormCard').style.display = 'block';
            this.style.display = 'none';
        });
    }

    const cancelAppointmentBtn = document.getElementById('cancelAppointment');
    if (cancelAppointmentBtn) {
        cancelAppointmentBtn.addEventListener('click', function() {
            document.getElementById('appointmentFormCard').style.display = 'none';
            document.getElementById('showAppointmentForm').style.display = 'block';
        });
    }
});