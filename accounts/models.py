from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _

class CustomUserManager(BaseUserManager):
    """Custom user manager supporting email/phone registration and authentication"""
    def create_user(self, email=None, phone=None, password=None, **extra_fields):
        if not email and not phone:
            raise ValueError(_("Either email or phone must be provided."))
        if email:
            email = self.normalize_email(email)
        
        # Ensure a username is assigned if not provided
        if not extra_fields.get('username'):
            extra_fields['username'] = email.split('@')[0] if email else f"user_{phone}"
            
        user = self.model(email=email, phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email=email, password=password, **extra_fields)


class CustomUser(AbstractUser):
    email = models.EmailField(_('email address'), unique=True, null=True, blank=True)
    phone = models.CharField(max_length=20, unique=True, null=True, blank=True)
    address = models.TextField(blank=True, null=True)
    city = models.CharField(max_length=100, default='Rajshahi')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = CustomUserManager()

    def __str__(self):
        return self.get_full_name() or self.email or self.phone or self.username


class Pet(models.Model):
    SPECIES_CHOICES = [
        ('Dog', 'Dog (কুকুর)'),
        ('Cat', 'Cat (বিড়াল)'),
        ('Bird', 'Bird (পাখি)'),
        ('Rabbit', 'Rabbit (খরগোশ)'),
        ('Fish', 'Fish (মাছ)'),
        ('Other', 'Other (অন্যান্য)'),
    ]

    GENDER_CHOICES = [
        ('Male', 'Male (পুরুষ)'),
        ('Female', 'Female (মহিলা)'),
        ('Unknown', 'Unknown (অজ্ঞাত)'),
    ]

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='pets')
    name = models.CharField(max_length=100)
    species = models.CharField(max_length=50, choices=SPECIES_CHOICES, default='Dog')
    breed = models.CharField(max_length=100, blank=True, null=True)
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='Unknown')
    age_years = models.PositiveIntegerField(default=0)
    age_months = models.PositiveIntegerField(default=0)
    weight_kg = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True)
    microchip_id = models.CharField(max_length=100, blank=True, null=True)
    medical_history = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='pets/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.species}) - Owner: {self.owner.get_full_name() or self.owner.username}"
