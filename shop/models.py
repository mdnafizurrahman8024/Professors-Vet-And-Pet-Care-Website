from django.db import models
from django.conf import settings
import uuid

class Category(models.Model):
    NAME_CHOICES = [
        ('Pet Food', 'Pet Food (খাবার)'),
        ('Veterinary Medicine', 'Veterinary Medicine (ওষুধ)'),
        ('Toys', 'Toys & Play (খেলনা)'),
        ('Accessories', 'Accessories & Collars (এক্সেসরিজ)'),
        ('Grooming & Hygiene', 'Grooming & Hygiene (পরিচর্যা)'),
    ]

    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=50, default="package", help_text="Lucide icon name")
    description = models.TextField(blank=True)
    image = models.ImageField(upload_to='categories/', blank=True, null=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['name']

    def __str__(self):
        return self.name


class Product(models.Model):
    PET_CHOICES = [
        ('ALL', 'All Pets (সকল পোষা প্রাণী)'),
        ('DOG', 'Dogs (কুকুর)'),
        ('CAT', 'Cats (বিড়াল)'),
        ('BIRD', 'Birds (পাখি)'),
        ('RABBIT', 'Rabbits (খরগোশ)'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True)
    sku = models.CharField(max_length=50, unique=True, help_text="Unique Stock Keeping Unit")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    target_pet = models.CharField(max_length=20, choices=PET_CHOICES, default='ALL')
    
    short_description = models.CharField(max_length=255, help_text="Brief highlight shown in product card")
    description = models.TextField(help_text="Detailed product specification and usage instructions")
    
    price = models.DecimalField(max_digits=10, decimal_places=2, help_text="Regular price in BDT")
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, help_text="Discounted price in BDT")
    
    stock_quantity = models.PositiveIntegerField(default=10, help_text="Units available in clinic inventory")
    is_prescription_required = models.BooleanField(
        default=False, 
        help_text="Check if this medicine requires doctor prescription upload"
    )
    
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    manufacturer = models.CharField(max_length=150, blank=True, default="Professor's Vet Care & Pharma")
    expiry_date = models.DateField(null=True, blank=True, help_text="Important for veterinary medicines")
    
    is_active = models.BooleanField(default=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-is_featured', '-created_at']

    def __str__(self):
        return f"{self.name} ({self.category.name}) - Stock: {self.stock_quantity}"

    @property
    def current_price(self):
        if self.discount_price and self.discount_price < self.price:
            return self.discount_price
        return self.price

    @property
    def has_discount(self):
        return bool(self.discount_price and self.discount_price < self.price)

    @property
    def discount_percentage(self):
        if self.has_discount and self.price > 0:
            pct = int(((self.price - self.discount_price) / self.price) * 100)
            return pct
        return 0

    @property
    def is_in_stock(self):
        return self.stock_quantity > 0

    @property
    def stock_status(self):
        if self.stock_quantity == 0:
            return 'out_of_stock'
        elif self.stock_quantity <= 5:
            return 'low_stock'
        return 'in_stock'


class Order(models.Model):
    STATUS_CHOICES = [
        ('PENDING', 'Pending (অপেক্ষমাণ)'),
        ('CONFIRMED', 'Confirmed (নিশ্চিত)'),
        ('PROCESSING', 'Processing (প্রক্রিয়াধীন)'),
        ('SHIPPED', 'Shipped / Out for Delivery (ডেলিভারিতে আছে)'),
        ('DELIVERED', 'Delivered (ডেলিভার সম্পন্ন)'),
        ('CANCELLED', 'Cancelled (বাতিল)'),
    ]

    PAYMENT_METHOD_CHOICES = [
        ('COD', 'Cash on Delivery (ক্যাশ অন ডেলিভারি)'),
        ('BKASH', 'bKash Online / Send Money (বিকাশ)'),
        ('NAGAD', 'Nagad Online (নগদ)'),
        ('CARD', 'Debit / Credit Card (ভিসা / মাস্টারকার্ড)'),
    ]

    PAYMENT_STATUS_CHOICES = [
        ('UNPAID', 'Unpaid (অপরিশোধিত)'),
        ('PAID', 'Paid (পরিশোধিত)'),
        ('REFUNDED', 'Refunded (ফেরত)'),
    ]

    order_number = models.CharField(max_length=32, unique=True, editable=False)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='orders'
    )
    
    # Billing & Shipping
    full_name = models.CharField(max_length=150)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    city = models.CharField(max_length=100, default="Rajshahi")
    postal_code = models.CharField(max_length=20, blank=True, default="6205")
    order_notes = models.TextField(blank=True, null=True)

    # Prescription for restricted meds
    prescription_file = models.FileField(upload_to='order_prescriptions/', blank=True, null=True)

    # Financials
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    delivery_fee = models.DecimalField(max_digits=10, decimal_places=2, default=60.00) # Inside Rajshahi
    total_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)

    # Payment
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, default='COD')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='UNPAID')
    transaction_id = models.CharField(max_length=100, blank=True, null=True, help_text="bKash/Nagad TrxID")
    
    # Order Lifecycle
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f"ORD-{uuid.uuid4().hex[:8].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.order_number} - {self.full_name} (BDT {self.total_amount})"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.product_name} x {self.quantity}"
