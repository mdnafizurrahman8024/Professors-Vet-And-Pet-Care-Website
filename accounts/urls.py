from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard_view, name='user_dashboard'),
    path('pets/add/', views.add_pet_view, name='add_pet'),
    path('pets/delete/<int:pet_id>/', views.delete_pet_view, name='delete_pet'),
    path('password-reset/', views.password_reset_view, name='password_reset'),
]
