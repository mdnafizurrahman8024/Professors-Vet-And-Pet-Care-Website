from django.db import models

class SurgeryCategory(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    description = models.TextField(blank=True)
    icon_name = models.CharField(max_length=50, default="activity")

    class Meta:
        verbose_name_plural = "Surgery Categories"

    def __str__(self):
        return self.name


class SurgeryCase(models.Model):
    title = models.CharField(max_length=200, help_text="Case Title (e.g. Femur Fracture Fixation in 2-Year-Old German Shepherd)")
    category = models.ForeignKey(SurgeryCategory, on_delete=models.CASCADE, related_name='cases')
    pet_name = models.CharField(max_length=100, blank=True, default="Patient Pet")
    pet_species = models.CharField(max_length=50, default="Dog")
    pet_breed = models.CharField(max_length=100, blank=True)
    chief_surgeon = models.CharField(max_length=150, default="Dr. Abdulla Al Mamun Bhuyan")
    
    case_summary = models.TextField(help_text="Diagnosis and initial clinical presentation")
    procedure_details = models.TextField(help_text="Surgical intervention and clinical procedure undertaken")
    recovery_outcome = models.TextField(help_text="Post-operative care and recovery outcome", default="Complete recovery within 4 weeks.")
    outcome = models.CharField(max_length=100, default="Successful Recovery")
    
    # Media
    primary_image = models.ImageField(upload_to='gallery/primary/', help_text="Main surgery display image", blank=True, null=True)
    before_image = models.ImageField(upload_to='gallery/before/', blank=True, null=True, help_text="Pre-treatment condition")
    after_image = models.ImageField(upload_to='gallery/after/', blank=True, null=True, help_text="Post-treatment condition")
    video_url = models.URLField(blank=True, null=True, help_text="Video walkthrough URL (YouTube, Vimeo, or MP4 link)")
    
    treatment_date = models.DateField()
    is_featured = models.BooleanField(default=False, help_text="Highlight on homepage showcase")
    is_published = models.BooleanField(default=True)
    view_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-is_featured', '-treatment_date', '-created_at']

    def __str__(self):
        return f"{self.title} ({self.pet_species}) - {self.category.name}"
