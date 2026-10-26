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
    map_satellite_embed_url = models.TextField(
        default="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3634.3904576352934!2d88.6366!3d24.3636!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x39fbefb8d601a9a7%3A0x6b87635b7190f845!2sDepartment%20of%20Veterinary%20and%20Animal%20Sciences!5e1!3m2!1sen!2sbd!4v1710000000000!5m2!1sen!2sbd"
    )
    operating_hours = models.CharField(max_length=255, default="Sat - Thu: 04:00 PM - 09:30 PM | Friday: 10:00 AM - 08:00 PM")
    emergency_contact = models.CharField(max_length=50, default="+8801316254500")

    def __str__(self):
        return self.clinic_name
