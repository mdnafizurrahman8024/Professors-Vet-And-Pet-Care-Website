from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils.crypto import get_random_string
from django.db.models import Q
from .models import CustomUser, Pet
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, PetForm
from .backends import EmailOrPhoneBackend
from appointments.models import Appointment
from shop.models import Order

def register_view(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')

    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            full_name = form.cleaned_data['full_name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            password = form.cleaned_data['password']

            # Split name into first and last
            parts = full_name.strip().split(' ', 1)
            first_name = parts[0]
            last_name = parts[1] if len(parts) > 1 else ''

            user = CustomUser.objects.create_user(
                email=email,
                phone=phone,
                password=password,
                first_name=first_name,
                last_name=last_name
            )

            # Log the user in
            backend = EmailOrPhoneBackend()
            authenticated_user = backend.authenticate(request, username=email, password=password)
            if authenticated_user:
                login(request, authenticated_user, backend='accounts.backends.EmailOrPhoneBackend')

            messages.success(request, f"Welcome to Professor's Vet & Pet Care, {first_name}! Your account has been registered.")
            
            # If user came from checkout or appointment, redirect back
            next_url = request.GET.get('next') or 'user_dashboard'
            return redirect(next_url)
    else:
        form = UserRegistrationForm()

    return render(request, 'accounts/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('user_dashboard')

    next_url = request.GET.get('next', 'user_dashboard')

    if request.method == 'POST':
        form = UserLoginForm(request.POST)
        if form.is_valid():
            login_credential = form.cleaned_data['login_credential']
            password = form.cleaned_data['password']
            remember_me = form.cleaned_data['remember_me']

            backend = EmailOrPhoneBackend()
            user = backend.authenticate(request, username=login_credential, password=password)

            if user is not None:
                login(request, user, backend='accounts.backends.EmailOrPhoneBackend')
                
                # Remember Me handling: 30 days vs session close
                if remember_me:
                    request.session.set_expiry(60 * 60 * 24 * 30) # 30 days
                else:
                    request.session.set_expiry(0) # Closes when browser exits

                messages.success(request, f"Welcome back, {user.first_name or user.username}!")
                return redirect(next_url if next_url else 'home')
            else:
                messages.error(request, "Invalid email/phone or password. Please verify and try again.")
    else:
        form = UserLoginForm()

    return render(request, 'accounts/login.html', {'form': form, 'next': next_url})


def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out securely. See you soon!")
    return redirect('home')


@login_required
def dashboard_view(request):
    user = request.user
    active_tab = request.GET.get('tab', 'profile')

    # Fetch user data
    pets = Pet.objects.filter(owner=user).order_by('-created_at')
    appointments = Appointment.objects.filter(Q(user=user) | Q(owner_email=user.email) | Q(owner_phone=user.phone)).distinct().order_by('-appointment_date', '-appointment_time')
    orders = Order.objects.filter(Q(user=user) | Q(email=user.email)).distinct().order_by('-created_at')

    # Profile Update handling
    if request.method == 'POST' and 'update_profile' in request.POST:
        profile_form = UserProfileForm(request.POST, request.FILES, instance=user)
        if profile_form.is_valid():
            profile_form.save()
            messages.success(request, "Your profile details have been updated successfully.")
            return redirect('/accounts/dashboard/?tab=profile')
    else:
        profile_form = UserProfileForm(instance=user)

    # Password Change handling
    if request.method == 'POST' and 'change_password' in request.POST:
        current_p = request.POST.get('current_password')
        new_p = request.POST.get('new_password')
        confirm_p = request.POST.get('confirm_password')

        if not user.check_password(current_p):
            messages.error(request, "Current password was incorrect.")
        elif len(new_p) < 6:
            messages.error(request, "New password must be at least 6 characters.")
        elif new_p != confirm_p:
            messages.error(request, "New passwords do not match.")
        else:
            user.set_password(new_p)
            user.save()
            update_session_auth_hash(request, user)
            messages.success(request, "Your password has been changed successfully!")
            return redirect('/accounts/dashboard/?tab=security')

    pet_form = PetForm()

    return render(request, 'accounts/dashboard.html', {
        'profile_form': profile_form,
        'pet_form': pet_form,
        'pets': pets,
        'appointments': appointments,
        'orders': orders,
        'active_tab': active_tab,
    })


@login_required
def add_pet_view(request):
    if request.method == 'POST':
        form = PetForm(request.POST, request.FILES)
        if form.is_valid():
            pet = form.save(commit=False)
            pet.owner = request.user
            pet.save()
            messages.success(request, f"Pet '{pet.name}' added to your profile!")
        else:
            messages.error(request, "Please check the pet details submitted.")
    return redirect('/accounts/dashboard/?tab=pets')


@login_required
def delete_pet_view(request, pet_id):
    pet = get_object_or_404(Pet, id=pet_id, owner=request.user)
    pet_name = pet.name
    pet.delete()
    messages.info(request, f"Pet profile for '{pet_name}' has been removed.")
    return redirect('/accounts/dashboard/?tab=pets')


def password_reset_view(request):
    """Secure account recovery simulation"""
    step = 'request'
    if request.method == 'POST':
        if 'request_reset' in request.POST:
            credential = request.POST.get('credential', '').strip()
            user = CustomUser.objects.filter(Q(email__iexact=credential) | Q(phone=credential)).first()
            if user:
                # In production, send email/SMS token. For seamless usability, generate temporary secure reset link
                token = get_random_string(32)
                request.session['reset_user_id'] = user.id
                request.session['reset_token'] = token
                messages.success(request, f"Password reset instructions have been generated for {user.email or user.phone}.")
                return render(request, 'accounts/password_reset.html', {'step': 'confirm', 'target_user': user})
            else:
                messages.error(request, "No account was found with that email or phone number.")
        elif 'confirm_reset' in request.POST:
            user_id = request.session.get('reset_user_id')
            new_password = request.POST.get('new_password')
            confirm_password = request.POST.get('confirm_password')

            if user_id and new_password and new_password == confirm_password and len(new_password) >= 6:
                user = CustomUser.objects.get(id=user_id)
                user.set_password(new_password)
                user.save()
                del request.session['reset_user_id']
                messages.success(request, "Your password has been reset successfully! You can now log in.")
                return redirect('login')
            else:
                messages.error(request, "Passwords must match and have at least 6 characters.")
                return render(request, 'accounts/password_reset.html', {'step': 'confirm'})

    return render(request, 'accounts/password_reset.html', {'step': step})
