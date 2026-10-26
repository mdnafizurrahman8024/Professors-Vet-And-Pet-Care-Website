from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.utils.dateparse import parse_date
from datetime import datetime, time, timedelta, date
from .models import DoctorSchedule, Appointment
from accounts.models import Pet

def get_slots_for_date(target_date):
    """
    Generate slots for the given date based on DoctorSchedule and existing appointments.
    """
    weekday = target_date.weekday() # Monday is 0, Sunday is 6
    schedule = DoctorSchedule.objects.filter(day_of_week=weekday, is_available=True).first()

    if not schedule:
        return []

    # Generate time slots
    slots = []
    start_dt = datetime.combine(target_date, schedule.start_time)
    end_dt = datetime.combine(target_date, schedule.end_time)
    duration = timedelta(minutes=schedule.slot_duration_minutes)

    # Existing booked appointments for this date
    booked_times = Appointment.objects.filter(
        appointment_date=target_date,
        status__in=['PENDING', 'CONFIRMED', 'IN_PROGRESS']
    ).values_list('appointment_time', flat=True)
    booked_set = set(t.strftime('%H:%M') for t in booked_times)

    current_dt = start_dt
    while current_dt + duration <= end_dt:
        time_str = current_dt.time().strftime('%H:%M')
        display_str = current_dt.time().strftime('%I:%M %p')
        is_available = time_str not in booked_set

        # If date is today, check if slot is already in the past
        if target_date == date.today() and current_dt.time() <= datetime.now().time():
            is_available = False

        slots.append({
            'time': time_str,
            'display': display_str,
            'is_available': is_available
        })
        current_dt += duration

    return slots


def available_slots_api(request):
    date_str = request.GET.get('date')
    if not date_str:
        return JsonResponse({'error': 'Date parameter required'}, status=400)
    
    target_date = parse_date(date_str)
    if not target_date or target_date < date.today():
        return JsonResponse({'slots': [], 'message': 'Please choose a future date.'})

    slots = get_slots_for_date(target_date)
    return JsonResponse({'slots': slots, 'date': date_str})


def book_appointment_view(request):
    user_pets = []
    initial_pet = None
    if request.user.is_authenticated:
        user_pets = Pet.objects.filter(owner=request.user)
        pet_id = request.GET.get('pet_id')
        if pet_id:
            initial_pet = user_pets.filter(id=pet_id).first()

    prefill_service = request.GET.get('service', '')

    if request.method == 'POST':
        owner_name = request.POST.get('owner_name')
        owner_phone = request.POST.get('owner_phone')
        owner_email = request.POST.get('owner_email')
        owner_address = request.POST.get('owner_address')
        
        pet_id = request.POST.get('pet_id')
        pet_name = request.POST.get('pet_name')
        pet_species = request.POST.get('pet_species', 'Dog')
        pet_breed = request.POST.get('pet_breed', '')
        pet_age = request.POST.get('pet_age', '')
        
        service_type = request.POST.get('service_type')
        date_str = request.POST.get('appointment_date')
        time_str = request.POST.get('appointment_time')
        symptoms = request.POST.get('symptoms', '')

        # Validations
        appointment_date = parse_date(date_str)
        if not appointment_date or appointment_date < date.today():
            messages.error(request, "Please pick a valid future appointment date.")
            return redirect('book_appointment')

        try:
            appointment_time = datetime.strptime(time_str, '%H:%M').time()
        except (ValueError, TypeError):
            messages.error(request, "Please choose an available time slot.")
            return redirect('book_appointment')

        # Check if already booked
        already_booked = Appointment.objects.filter(
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            status__in=['PENDING', 'CONFIRMED']
        ).exists()

        if already_booked:
            messages.error(request, "Sorry, this slot was just taken. Please select another slot.")
            return redirect('book_appointment')

        pet_obj = None
        if pet_id and request.user.is_authenticated:
            pet_obj = user_pets.filter(id=pet_id).first()
            if pet_obj and not pet_name:
                pet_name = pet_obj.name
                pet_species = pet_obj.species
                pet_breed = pet_obj.breed or ''

        appointment = Appointment.objects.create(
            user=request.user if request.user.is_authenticated else None,
            pet=pet_obj,
            owner_name=owner_name,
            owner_phone=owner_phone,
            owner_email=owner_email,
            owner_address=owner_address,
            pet_name=pet_name or (pet_obj.name if pet_obj else "Pet"),
            pet_species=pet_species,
            pet_breed=pet_breed,
            pet_age=pet_age,
            service_type=service_type,
            appointment_date=appointment_date,
            appointment_time=appointment_time,
            symptoms=symptoms,
            status='PENDING'
        )

        messages.success(request, f"Appointment successfully scheduled! Your reference ID is {appointment.booking_id}.")
        return redirect('appointment_success', booking_id=appointment.booking_id)

    # Defaults
    tomorrow = (date.today() + timedelta(days=1)).strftime('%Y-%m-%d')

    return render(request, 'appointments/book.html', {
        'user_pets': user_pets,
        'initial_pet': initial_pet,
        'prefill_service': prefill_service,
        'min_date': date.today().strftime('%Y-%m-%d'),
        'default_date': tomorrow,
        'service_choices': Appointment.SERVICE_CHOICES,
    })


def appointment_success_view(request, booking_id):
    appointment = get_object_or_404(Appointment, booking_id=booking_id)
    return render(request, 'appointments/success.html', {'appointment': appointment})
