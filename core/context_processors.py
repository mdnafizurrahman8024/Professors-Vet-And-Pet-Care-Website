from .models import NoticeOffer, ClinicInfo

def global_context(request):
    try:
        clinic = ClinicInfo.objects.first()
        if not clinic:
            clinic = ClinicInfo()
            
        marquee_notices = NoticeOffer.objects.filter(is_active=True, is_marquee=True)
        banner_offers = NoticeOffer.objects.filter(is_active=True, is_banner=True)
    except Exception:
        clinic = None
        marquee_notices = []
        banner_offers = []

    return {
        'clinic': clinic,
        'marquee_notices': marquee_notices,
        'banner_offers': banner_offers,
    }
