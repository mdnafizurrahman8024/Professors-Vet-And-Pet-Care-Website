from django.contrib import admin
from .models import NoticeOffer, ClinicInfo

@admin.register(NoticeOffer)
class NoticeOfferAdmin(admin.ModelAdmin):
    list_display = ('title', 'badge_text', 'badge_type', 'is_marquee', 'is_banner', 'discount_code', 'is_active', 'priority', 'created_at')
    list_editable = ('is_marquee', 'is_banner', 'is_active', 'priority')
    list_filter = ('badge_type', 'is_active', 'is_marquee', 'is_banner')
    search_fields = ('title', 'content', 'discount_code')


@admin.register(ClinicInfo)
class ClinicInfoAdmin(admin.ModelAdmin):
    list_display = ('clinic_name', 'doctor_name', 'cell_number', 'email', 'clinic_physical_address')
