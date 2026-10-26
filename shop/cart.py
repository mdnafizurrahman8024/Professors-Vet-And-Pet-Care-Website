from decimal import Decimal
from .models import Product

class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get('cart')
        if not cart:
            cart = self.session['cart'] = {}
        self.cart = cart

    def add(self, product, quantity=1, override_quantity=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {
                'quantity': 0,
                'price': str(product.current_price),
                'name': product.name,
                'image_url': product.image.url if product.image else '',
                'stock': product.stock_quantity,
                'prescription_required': product.is_prescription_required,
                'sku': product.sku,
            }

        # Check stock limits
        max_allowed = product.stock_quantity
        if override_quantity:
            new_qty = min(quantity, max_allowed)
        else:
            new_qty = min(self.cart[product_id]['quantity'] + quantity, max_allowed)

        if new_qty > 0:
            self.cart[product_id]['quantity'] = new_qty
            self.cart[product_id]['price'] = str(product.current_price)
            self.cart[product_id]['stock'] = product.stock_quantity
            self.save()
            return True, new_qty
        else:
            return False, 0

    def remove(self, product):
        product_id = str(product.id)
        if product_id in self.cart:
            del self.cart[product_id]
            self.save()

    def update_quantity(self, product_id, quantity):
        product_id = str(product_id)
        if product_id in self.cart:
            if quantity > 0:
                try:
                    product = Product.objects.get(id=int(product_id))
                    qty = min(quantity, product.stock_quantity)
                    self.cart[product_id]['quantity'] = qty
                    self.cart[product_id]['stock'] = product.stock_quantity
                    self.cart[product_id]['price'] = str(product.current_price)
                except Product.DoesNotExist:
                    self.cart[product_id]['quantity'] = quantity
            else:
                del self.cart[product_id]
            self.save()

    def save(self):
        self.session.modified = True

    def clear(self):
        del self.session['cart']
        self.save()

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(id__in=product_ids)
        cart = self.cart.copy()

        for product in products:
            cart[str(product.id)]['product'] = product

        for item in cart.values():
            item['price'] = Decimal(item['price'])
            item['total_price'] = item['price'] * item['quantity']
            yield item

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    def get_subtotal(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    def has_prescription_items(self):
        for item in self.cart.values():
            if item.get('prescription_required'):
                return True
        return False
