from django.shortcuts import render
from shop.models import Product
from gallery.models import SurgeryCase
from .models import NoticeOffer, ClinicInfo

def home(request):
    featured_products = Product.objects.filter(is_active=True, is_featured=True)[:8]
    if not featured_products.exists():
        # Fallback to any active products if none marked featured
        featured_products = Product.objects.filter(is_active=True)[:8]

    featured_cases = SurgeryCase.objects.filter(is_published=True, is_featured=True)[:3]
    if not featured_cases.exists():
        featured_cases = SurgeryCase.objects.filter(is_published=True)[:3]

    return render(request, 'core/home.html', {
        'featured_products': featured_products,
        'featured_cases': featured_cases,
    })
