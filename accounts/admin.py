from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Pet

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('username', 'email', 'phone', 'first_name', 'last_name', 'city', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active', 'city')
    search_fields = ('username', 'email', 'phone', 'first_name', 'last_name')
    ordering = ('-date_joined',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Clinic Profile & Contact', {'fields': ('phone', 'address', 'city', 'avatar', 'is_verified')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Clinic Profile & Contact', {'fields': ('email', 'phone', 'address', 'city')}),
    )


@admin.register(Pet)
class PetAdmin(admin.ModelAdmin):
    list_display = ('name', 'species', 'breed', 'gender', 'owner', 'age_years', 'age_months', 'weight_kg', 'created_at')
    list_filter = ('species', 'gender')
    search_fields = ('name', 'breed', 'owner__email', 'owner__phone', 'owner__username')
