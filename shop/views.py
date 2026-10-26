import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from .models import Category, Product, Order, OrderItem
from .cart import Cart

def shop_home(request):
    categories = Category.objects.all()
    selected_category = request.GET.get('category')
    selected_pet = request.GET.get('pet')
    search_query = request.GET.get('q')
    sort_by = request.GET.get('sort', 'featured')

    products = Product.objects.filter(is_active=True)

    if selected_category:
        products = products.filter(category__slug=selected_category)

    if selected_pet:
        products = products.filter(Q(target_pet__iexact=selected_pet) | Q(target_pet='ALL'))

    if search_query:
        products = products.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(sku__icontains=search_query) |
            Q(manufacturer__icontains=search_query)
        )

    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'newest':
        products = products.order_by('-created_at')
    else:
        products = products.order_by('-is_featured', '-created_at')

    return render(request, 'shop/home.html', {
        'products': products,
        'categories': categories,
        'selected_category': selected_category,
        'selected_pet': selected_pet,
        'search_query': search_query,
        'sort_by': sort_by,
    })


def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug, is_active=True)
    related_products = Product.objects.filter(
        category=product.category, 
        is_active=True
    ).exclude(id=product.id)[:4]

    return render(request, 'shop/product_detail.html', {
        'product': product,
        'related_products': related_products,
    })


def cart_add_ajax(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        quantity = int(data.get('quantity', 1))

        product = get_object_or_404(Product, id=product_id, is_active=True)

        if product.stock_quantity <= 0:
            return JsonResponse({
                'status': 'error', 
                'message': f"Sorry, '{product.name}' is currently out of stock."
            })

        cart = Cart(request)
        current_in_cart = cart.cart.get(str(product.id), {}).get('quantity', 0)
        
        if current_in_cart + quantity > product.stock_quantity:
            allowed_more = max(0, product.stock_quantity - current_in_cart)
            if allowed_more == 0:
                return JsonResponse({
                    'status': 'error',
                    'message': f"You already have the maximum available stock ({product.stock_quantity}) of '{product.name}' in your cart."
                })
            quantity = allowed_more

        success, new_qty = cart.add(product=product, quantity=quantity)

        remaining = product.stock_quantity - new_qty

        return JsonResponse({
            'status': 'success',
            'message': f"Added '{product.name}' to cart!",
            'cart_count': len(cart),
            'cart_subtotal': str(cart.get_subtotal()),
            'quantity_in_cart': new_qty,
            'remaining_stock': remaining,
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def cart_update_ajax(request):
    if request.method != 'POST':
        return JsonResponse({'status': 'error', 'message': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        product_id = data.get('product_id')
        action = data.get('action') # 'increase', 'decrease', or 'remove'
        
        cart = Cart(request)
        item = cart.cart.get(str(product_id))

        if not item:
            return JsonResponse({'status': 'error', 'message': 'Item not in cart'}, status=404)

        product = get_object_or_404(Product, id=product_id)

        if action == 'increase':
            if item['quantity'] < product.stock_quantity:
                cart.update_quantity(product_id, item['quantity'] + 1)
            else:
                return JsonResponse({
                    'status': 'error', 
                    'message': f"Cannot add more than available stock ({product.stock_quantity})."
                })
        elif action == 'decrease':
            new_qty = item['quantity'] - 1
            if new_qty > 0:
                cart.update_quantity(product_id, new_qty)
            else:
                cart.remove(product)
        elif action == 'remove':
            cart.remove(product)

        delivery_fee = Decimal('60.00') if len(cart) > 0 else Decimal('0.00')
        subtotal = cart.get_subtotal()
        total = subtotal + delivery_fee

        return JsonResponse({
            'status': 'success',
            'cart_count': len(cart),
            'cart_subtotal': str(subtotal),
            'delivery_fee': str(delivery_fee),
            'total': str(total),
        })
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


def cart_detail(request):
    cart = Cart(request)
    subtotal = cart.get_subtotal()
    delivery_fee = Decimal('60.00') if len(cart) > 0 else Decimal('0.00')
    total = subtotal + delivery_fee

    return render(request, 'shop/cart.html', {
        'cart': cart,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'total': total,
        'has_prescription_items': cart.has_prescription_items(),
    })


def check_stock_api(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    return JsonResponse({
        'id': product.id,
        'stock_quantity': product.stock_quantity,
        'is_in_stock': product.is_in_stock,
        'status': product.stock_status,
        'price': str(product.current_price)
    })


def checkout_view(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.warning(request, "Your shopping cart is currently empty.")
        return redirect('shop_home')

    is_guest = request.GET.get('guest') == '1' or not request.user.is_authenticated

    subtotal = cart.get_subtotal()
    delivery_fee = Decimal('60.00')
    total_amount = subtotal + delivery_fee

    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        shipping_address = request.POST.get('shipping_address')
        city = request.POST.get('city', 'Rajshahi')
        postal_code = request.POST.get('postal_code', '6205')
        order_notes = request.POST.get('order_notes', '')
        payment_method = request.POST.get('payment_method', 'COD')
        transaction_id = request.POST.get('transaction_id', '')
        prescription_file = request.FILES.get('prescription_file')

        # Prescription check
        if cart.has_prescription_items() and not prescription_file:
            messages.error(request, "One or more items in your cart require a veterinary prescription upload.")
            return render(request, 'shop/checkout.html', {
                'cart': cart,
                'subtotal': subtotal,
                'delivery_fee': delivery_fee,
                'total_amount': total_amount,
                'is_guest': is_guest,
            })

        # Atomic transaction to guarantee stock consistency
        with transaction.atomic():
            # 1. Real-time stock verification & lock check
            for item in cart:
                prod = Product.objects.select_for_update().get(id=item['product'].id)
                if prod.stock_quantity < item['quantity']:
                    messages.error(
                        request, 
                        f"Sorry! '{prod.name}' only has {prod.stock_quantity} units available now. Please adjust your cart."
                    )
                    return redirect('cart_detail')

            # 2. Determine initial payment status
            payment_status = 'PAID' if payment_method in ['BKASH', 'NAGAD', 'CARD'] and transaction_id else 'UNPAID'

            # 3. Create Order
            order = Order.objects.create(
                user=request.user if request.user.is_authenticated else None,
                full_name=full_name,
                email=email,
                phone=phone,
                shipping_address=shipping_address,
                city=city,
                postal_code=postal_code,
                order_notes=order_notes,
                subtotal=subtotal,
                delivery_fee=delivery_fee,
                total_amount=total_amount,
                payment_method=payment_method,
                payment_status=payment_status,
                transaction_id=transaction_id if transaction_id else None,
                prescription_file=prescription_file,
                status='PENDING'
            )

            # 4. Create OrderItems & Decrement Inventory
            for item in cart:
                prod = Product.objects.select_for_update().get(id=item['product'].id)
                OrderItem.objects.create(
                    order=order,
                    product=prod,
                    product_name=prod.name,
                    price=item['price'],
                    quantity=item['quantity'],
                    total_price=item['total_price']
                )
                # Decrement stock in database
                prod.stock_quantity = max(0, prod.stock_quantity - item['quantity'])
                prod.save(update_fields=['stock_quantity', 'updated_at'])

            # 5. Clear session cart
            cart.clear()

        messages.success(request, f"Order #{order.order_number} has been placed successfully!")
        return redirect('order_confirmation', order_number=order.order_number)

    return render(request, 'shop/checkout.html', {
        'cart': cart,
        'subtotal': subtotal,
        'delivery_fee': delivery_fee,
        'total_amount': total_amount,
        'is_guest': is_guest,
    })


def order_confirmation_view(request, order_number):
    order = get_object_or_404(Order, order_number=order_number)
    return render(request, 'shop/confirmation.html', {'order': order})
