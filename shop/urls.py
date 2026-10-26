from django.urls import path
from . import views

urlpatterns = [
    path('', views.shop_home, name='shop_home'),
    path('cart/', views.cart_detail, name='cart_detail'),
    path('cart/add/', views.cart_add_ajax, name='cart_add_ajax'),
    path('cart/update/', views.cart_update_ajax, name='cart_update_ajax'),
    path('checkout/', views.checkout_view, name='checkout'),
    path('order/confirmation/<str:order_number>/', views.order_confirmation_view, name='order_confirmation'),
    path('api/stock/<int:product_id>/', views.check_stock_api, name='check_stock_api'),
    path('product/<slug:slug>/', views.product_detail, name='product_detail'),
]
