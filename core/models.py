from django.db import models

class NoticeOffer(models.Model):
    BADGE_TYPES = [
        ('OFFER', 'Special Offer (অফার)'),
        ('NOTICE', 'Clinic Notice (বিজ্ঞপ্তি)'),
        ('CAMP', 'Free Health Camp (ক্যাম্প)'),
        ('EMERGENCY', 'Emergency Alert (জরুরী সতর্কতা)'),
    ]

    title = models.CharField(max_length=255)
    content = models.TextField(help_text="Detailed message or offer details")
    badge_text = models.CharField(max_length=50, default="HOT OFFER")
    badge_type = models.CharField(max_length=20, choices=BADGE_TYPES, default='OFFER')
    is_marquee = models.BooleanField(default=True, help_text="Show in the top moving announcement ticker")
    is_banner = models.BooleanField(default=True, help_text="Show in the hero offer cards")
    discount_code = models.CharField(max_length=50, blank=True, null=True, help_text="e.g. VETCARE20")
    discount_percentage = models.PositiveIntegerField(blank=True, null=True, help_text="e.g. 15 for 15% off")
    link_url = models.CharField(max_length=255, blank=True, null=True, default="/shop/")
    is_active = models.BooleanField(default=True)
    priority = models.IntegerField(default=0, help_text="Higher priority items appear first")
    start_date = models.DateTimeField(null=True, blank=True)
    end_date = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-priority', '-created_at']

    def __str__(self):
        return f"[{self.badge_text}] {self.title}"


class ClinicInfo(models.Model):
    clinic_name = models.CharField(max_length=200, default="Professor's Vet & Pet Care")
    tagline = models.CharField(max_length=255, default="Expert Veterinary Medicine, Surgery & Premium Pet Care in Rajshahi")
    doctor_name = models.CharField(max_length=200, default="Dr. Abdulla Al Mamun Bhuyan")
    doctor_degrees = models.CharField(max_length=255, default="DVM, MS (BAU), Dr.sc.hum (Germany)")
    doctor_designation = models.CharField(
        max_length=255, 
        default="Associate Professor, Department of Veterinary and Animal Sciences"
    )
    doctor_institution = models.CharField(
        max_length=255, 
        default="University of Rajshahi, Rajshahi-6205, Bangladesh"
    )
    cell_number = models.CharField(max_length=50, default="+8801316254500")
    email = models.EmailField(default="bhuyan@ru.ac.bd")
    chamber_address = models.TextField(
        default="Department of Veterinary and Animal Sciences, University of Rajshahi, Rajshahi-6205, Bangladesh."
    )
    clinic_physical_address = models.TextField(
        default="138 Debishing Para, Madrashar More, Rajshahi"
    )
    map_latitude = models.DecimalField(max_digits=18, decimal_places=15, default=24.367926395092578)
    map_longitude = models.DecimalField(max_digits=18, decimal_places=15, default=88.62464757770542)
    map_satellite_embed_url = models.TextField(
        default="https://maps.google.com/maps?q=Professor%27s%20Vet%20%26%20Pet%20Care%4024.367926395092578,88.62464757770542&t=k&z=18&ie=UTF8&iwloc=&output=embed"
    )
    operating_hours = models.CharField(max_length=255, default="Sat - Thu: 04:00 PM - 09:30 PM | Friday: 10:00 AM - 08:00 PM")
    emergency_contact = models.CharField(max_length=50, default="+8801316254500")

    def __str__(self):
        return self.clinic_name
