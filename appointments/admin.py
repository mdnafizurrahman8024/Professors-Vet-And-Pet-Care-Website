from django.contrib import admin
from .models import DoctorSchedule, Appointment

@admin.register(DoctorSchedule)
class DoctorScheduleAdmin(admin.ModelAdmin):
    list_display = ('day_of_week', 'start_time', 'end_time', 'slot_duration_minutes', 'max_patients_per_slot', 'is_available', 'notes')
    list_editable = ('is_available', 'start_time', 'end_time', 'slot_duration_minutes')
    ordering = ('day_of_week',)


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = (
        'booking_id', 'pet_name', 'pet_species', 'owner_name', 'owner_phone', 
        'service_type', 'appointment_date', 'appointment_time', 'status', 'is_paid'
    )
    list_editable = ('status', 'is_paid')
    list_filter = ('status', 'appointment_date', 'service_type', 'is_paid', 'pet_species')
    search_fields = ('booking_id', 'pet_name', 'owner_name', 'owner_phone', 'owner_email', 'symptoms')
    date_hierarchy = 'appointment_date'
    actions = ['mark_confirmed', 'mark_completed', 'mark_cancelled']

    @admin.action(description="Mark selected appointments as Confirmed")
    def mark_confirmed(self, request, queryset):
        queryset.update(status='CONFIRMED')

    @admin.action(description="Mark selected appointments as Completed")
    def mark_completed(self, request, queryset):
        queryset.update(status='COMPLETED')

    @admin.action(description="Mark selected appointments as Cancelled")
    def mark_cancelled(self, request, queryset):
        queryset.update(status='CANCELLED')
