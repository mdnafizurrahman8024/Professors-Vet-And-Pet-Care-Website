from django.db import models
from django.conf import settings
import uuid
import datetime

class DoctorSchedule(models.Model):
    DAY_CHOICES = [
        (5, 'Saturday (শনিবার)'),
        (6, 'Sunday (রবিবার)'),
        (0, 'Monday (সোমবার)'),
        (1, 'Tuesday (মঙ্গলবার)'),
        (2, 'Wednesday (বুধবার)'),
        (3, 'Thursday (বৃহস্পতিবার)'),
        (4, 'Friday (শুক্রবার)'),
    ]

    day_of_week = models.IntegerField(choices=DAY_CHOICES, unique=True)
    is_available = models.BooleanField(default=True)
    start_time = models.TimeField(default="16:00")
    end_time = models.TimeField(default="21:30")
    slot_duration_minutes = models.PositiveIntegerField(default=20)
    max_patients_per_slot = models.PositiveIntegerField(default=1)
    notes = models.CharField(max_length=255, blank=True, default="Standard Chamber Hours")

    class Meta:
        ordering = ['day_of_week']

    def __str__(self):
        day_name = dict(self.DAY_CHOICES).get(self.day_of_week, str(self.day_of_week))
        status = "Active" if self.is_available else "Off-Day"
        return f"{day_name} ({self.start_time.strftime('%I:%M %p')} - {self.end_time.strftime('%I:%M %p')}) - [{status}]"


class Appointment(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending Confirmation (অপেক্ষমাণ)'),
        ('CONFIRMED', 'Confirmed (নিশ্চিত)'),
        ('IN_PROGRESS', 'In Progress (চলমান)'),
        ('COMPLETED', 'Completed (সম্পন্ন)'),
        ('CANCELLED', 'Cancelled (বাতিল)'),
    ]

    SERVICE_CHOICES = [
        ('General Health Checkup', 'General Health Checkup (সাধারণ স্বাস্থ্য পরীক্ষা)'),
        ('Vaccination & Deworming', 'Vaccination & Deworming (টিকা ও কৃমিনাশক)'),
        ('Minor/Major Surgery Consultation', 'Minor/Major Surgery Consultation (সার্জারি পরামর্শ)'),
        ('Orthopedic & Bone Treatment', 'Orthopedic & Fracture Care (অর্থোপেডিক ও হাড় চিকিৎসা)'),
        ('Dental & Oral Hygiene', 'Dental & Oral Hygiene (দাঁতের চিকিৎসা)'),
        ('Emergency & Trauma Care', 'Emergency & Trauma Care (জরুরী ট্রমা কেয়ার)'),
        ('Skin & Dermatology Care', 'Skin & Allergy Care (চর্মরোগ ও অ্যালার্জি)'),
        ('Ultrasound & Diagnostic Followup', 'Diagnostic Followup (ডায়াগনস্টিক রিপোর্ট মূল্যায়ন)'),
    ]

    booking_id = models.CharField(max_length=20, unique=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='appointments'
    )
    pet = models.ForeignKey(
        'accounts.Pet', 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='appointments'
    )
    
    # Patient & Owner details
    owner_name = models.CharField(max_length=150)
    owner_phone = models.CharField(max_length=20)
    owner_email = models.EmailField(blank=True, null=True)
    owner_address = models.CharField(max_length=255, blank=True, null=True)
    
    pet_name = models.CharField(max_length=100)
    pet_species = models.CharField(max_length=50, default='Dog')
    pet_breed = models.CharField(max_length=100, blank=True, null=True)
    pet_age = models.CharField(max_length=50, blank=True, null=True)
    
    service_type = models.CharField(max_length=150, choices=SERVICE_CHOICES)
    appointment_date = models.DateField()
    appointment_time = models.TimeField()
    symptoms = models.TextField(help_text="Describe symptoms or reasons for visit")
    
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    doctor_advice = models.TextField(blank=True, null=True)
    prescribed_medicines = models.TextField(blank=True, null=True)
    is_paid = models.BooleanField(default=False)
    consultation_fee = models.DecimalField(max_digits=8, decimal_places=2, default=500.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-appointment_date', '-appointment_time']

    def save(self, *args, **kwargs):
        if not self.booking_id:
            # Generate unique reference APT-YYMM-XXXX
            today_str = datetime.date.today().strftime('%y%m')
            random_code = uuid.uuid4().hex[:5].upper()
            self.booking_id = f"APT-{today_str}-{random_code}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"[{self.booking_id}] {self.pet_name} ({self.owner_name}) - {self.appointment_date} {self.appointment_time.strftime('%I:%M %p')}"
