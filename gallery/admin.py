from django.contrib import admin
from .models import SurgeryCategory, SurgeryCase

@admin.register(SurgeryCategory)
class SurgeryCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(SurgeryCase)
class SurgeryCaseAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'category', 'pet_species', 'chief_surgeon', 
        'treatment_date', 'outcome', 'is_featured', 'is_published', 'view_count'
    )
    list_editable = ('is_featured', 'is_published')
    list_filter = ('category', 'pet_species', 'is_featured', 'is_published', 'treatment_date')
    search_fields = ('title', 'case_summary', 'procedure_details', 'pet_species', 'chief_surgeon')
    date_hierarchy = 'treatment_date'
