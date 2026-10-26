from django.urls import path
from . import views

urlpatterns = [
    path('book/', views.book_appointment_view, name='book_appointment'),
    path('api/available-slots/', views.available_slots_api, name='available_slots_api'),
    path('confirmation/<str:booking_id>/', views.appointment_success_view, name='appointment_success'),
]
