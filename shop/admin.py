from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Product, Order, OrderItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'icon', 'description')
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'name', 'category', 'target_pet', 'price', 'discount_price', 
        'stock_quantity', 'stock_badge', 'is_prescription_required', 
        'is_active', 'is_featured'
    )
    list_editable = ('price', 'discount_price', 'stock_quantity', 'is_active', 'is_featured')
    list_filter = ('category', 'target_pet', 'is_prescription_required', 'is_active', 'is_featured')
    search_fields = ('name', 'sku', 'description', 'manufacturer')
    prepopulated_fields = {'slug': ('name',)}

    @admin.display(description="Stock Status")
    def stock_badge(self, obj):
        if obj.stock_quantity == 0:
            return format_html('<span style="color:red; font-weight:bold;">{}</span>', 'Out of Stock (0)')
        elif obj.stock_quantity <= 5:
            return format_html('<span style="color:orange; font-weight:bold;">Low Stock ({})</span>', obj.stock_quantity)
        return format_html('<span style="color:green; font-weight:bold;">In Stock ({})</span>', obj.stock_quantity)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product_name', 'price', 'quantity', 'total_price')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number', 'full_name', 'phone', 'total_amount', 
        'payment_method', 'payment_status', 'status', 'created_at'
    )
    list_editable = ('status', 'payment_status')
    list_filter = ('status', 'payment_status', 'payment_method', 'created_at')
    search_fields = ('order_number', 'full_name', 'phone', 'email', 'transaction_id', 'shipping_address')
    inlines = [OrderItemInline]
    date_hierarchy = 'created_at'
    actions = ['mark_confirmed', 'mark_shipped', 'mark_delivered', 'mark_paid']

    @admin.action(description="Mark selected orders as Confirmed")
    def mark_confirmed(self, request, queryset):
        queryset.update(status='CONFIRMED')

    @admin.action(description="Mark selected orders as Shipped")
    def mark_shipped(self, request, queryset):
        queryset.update(status='SHIPPED')

    @admin.action(description="Mark selected orders as Delivered")
    def mark_delivered(self, request, queryset):
        queryset.update(status='DELIVERED')

    @admin.action(description="Mark selected orders as Paid")
    def mark_paid(self, request, queryset):
        queryset.update(payment_status='PAID')
