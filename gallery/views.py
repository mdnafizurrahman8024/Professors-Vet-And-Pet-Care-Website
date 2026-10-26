from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .models import SurgeryCategory, SurgeryCase

def gallery_list(request):
    categories = SurgeryCategory.objects.all()
    selected_category = request.GET.get('category')
    search_query = request.GET.get('q')

    cases = SurgeryCase.objects.filter(is_published=True)

    if selected_category:
        cases = cases.filter(category__slug=selected_category)

    if search_query:
        cases = cases.filter(
            Q(title__icontains=search_query) |
            Q(case_summary__icontains=search_query) |
            Q(pet_species__icontains=search_query) |
            Q(procedure_details__icontains=search_query)
        )

    return render(request, 'gallery/list.html', {
        'categories': categories,
        'cases': cases,
        'selected_category': selected_category,
        'search_query': search_query,
    })


def gallery_detail(request, case_id):
    case = get_object_or_404(SurgeryCase, id=case_id, is_published=True)
    # Increment view count
    case.view_count += 1
    case.save(update_fields=['view_count'])

    related_cases = SurgeryCase.objects.filter(
        category=case.category, 
        is_published=True
    ).exclude(id=case.id)[:3]

    return render(request, 'gallery/detail.html', {
        'case': case,
        'related_cases': related_cases,
    })
