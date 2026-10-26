from django.urls import path
from . import views

urlpatterns = [
    path('', views.gallery_list, name='gallery_list'),
    path('<int:case_id>/', views.gallery_detail, name='gallery_detail'),
]
