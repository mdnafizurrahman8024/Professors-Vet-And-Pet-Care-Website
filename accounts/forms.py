from django import forms
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from .models import CustomUser, Pet

class UserRegistrationForm(forms.ModelForm):
    full_name = forms.CharField(
        max_length=150, 
        required=True, 
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-sm focus:ring-2 focus:ring-brand-500 focus:outline-none',
            'placeholder': 'Enter your full name'
        })
    )
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-sm focus:ring-2 focus:ring-brand-500 focus:outline-none',
            'placeholder': 'name@example.com'
        })
    )
    phone = forms.CharField(
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-sm focus:ring-2 focus:ring-brand-500 focus:outline-none',
            'placeholder': '+8801XXXXXXXXX'
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-sm focus:ring-2 focus:ring-brand-500 focus:outline-none',
            'placeholder': 'Create strong password (min 6 characters)'
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-sm focus:ring-2 focus:ring-brand-500 focus:outline-none',
            'placeholder': 'Confirm password'
        })
    )

    class Meta:
        model = CustomUser
        fields = ['full_name', 'email', 'phone', 'password']

    def clean_email(self):
        email = self.cleaned_data.get('email').strip().lower()
        if CustomUser.objects.filter(email__iexact=email).exists():
            raise ValidationError("An account with this email already exists.")
        return email

    def clean_phone(self):
        phone = self.cleaned_data.get('phone').strip()
        if CustomUser.objects.filter(phone=phone).exists():
            raise ValidationError("An account with this phone number already exists.")
        return phone

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get('password')
        p2 = cleaned_data.get('confirm_password')
        if p1 and p2 and p1 != p2:
            self.add_error('confirm_password', "Passwords do not match.")
        return cleaned_data


class UserLoginForm(forms.Form):
    login_credential = forms.CharField(
        label="Email or Phone Number",
        widget=forms.TextInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-sm focus:ring-2 focus:ring-brand-500 focus:outline-none',
            'placeholder': 'Enter your email or phone number'
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            'class': 'w-full px-4 py-3 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-800 dark:text-slate-100 text-sm focus:ring-2 focus:ring-brand-500 focus:outline-none',
            'placeholder': 'Enter your password'
        })
    )
    remember_me = forms.BooleanField(
        required=False,
        initial=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'w-4 h-4 rounded text-brand-600 focus:ring-brand-500 border-slate-300 dark:border-slate-700'
        })
    )


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'email', 'phone', 'address', 'city', 'avatar']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm'}),
            'last_name': forms.TextInput(attrs={'class': 'w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm'}),
            'email': forms.EmailInput(attrs={'class': 'w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm'}),
            'phone': forms.TextInput(attrs={'class': 'w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm'}),
            'address': forms.Textarea(attrs={'class': 'w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm', 'rows': 2}),
            'city': forms.TextInput(attrs={'class': 'w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm'}),
            'avatar': forms.FileInput(attrs={'class': 'w-full text-xs text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100'}),
        }


class PetForm(forms.ModelForm):
    class Meta:
        model = Pet
        fields = ['name', 'species', 'breed', 'gender', 'age_years', 'age_months', 'weight_kg', 'medical_history', 'photo']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm', 'placeholder': "Pet's name"}),
            'species': forms.Select(attrs={'class': 'w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm'}),
            'breed': forms.TextInput(attrs={'class': 'w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm', 'placeholder': "e.g. Persian, German Shepherd, Local"}),
            'gender': forms.Select(attrs={'class': 'w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm'}),
            'age_years': forms.NumberInput(attrs={'class': 'w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm', 'min': 0}),
            'age_months': forms.NumberInput(attrs={'class': 'w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm', 'min': 0, 'max': 11}),
            'weight_kg': forms.NumberInput(attrs={'class': 'w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm', 'step': '0.1', 'placeholder': "Weight in kg"}),
            'medical_history': forms.Textarea(attrs={'class': 'w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-sm', 'rows': 3, 'placeholder': "Vaccination history, past surgeries, known allergies..."}),
            'photo': forms.FileInput(attrs={'class': 'w-full text-xs text-slate-500 file:mr-4 file:py-2 file:px-4 file:rounded-xl file:border-0 file:text-xs file:font-semibold file:bg-brand-50 file:text-brand-700 hover:file:bg-brand-100'}),
        }
