// Global Shopping Cart & Live Inventory Management JS
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function showToastNotification(message, type = 'success') {
    const existing = document.getElementById('global-toast-container');
    let container = existing;
    if (!container) {
        container = document.createElement('div');
        container.id = 'global-toast-container';
        container.className = 'fixed bottom-5 right-5 z-50 flex flex-col gap-2 pointer-events-none';
        document.body.appendChild(container);
    }

    const toast = document.createElement('div');
    const isError = type === 'error';
    const bgClass = isError ? 'bg-rose-600 text-white' : 'bg-emerald-600 text-white';
    const iconClass = isError ? 'fa-circle-exclamation' : 'fa-circle-check';

    toast.className = `${bgClass} px-4 py-3 rounded-xl shadow-xl flex items-center gap-2 text-xs font-semibold transform transition-all duration-300 translate-y-4 opacity-0 pointer-events-auto max-w-sm`;
    toast.innerHTML = `<i class="fa-solid ${iconClass} text-sm"></i> <span>${message}</span>`;
    
    container.appendChild(toast);

    // Animate in
    setTimeout(() => {
        toast.classList.remove('translate-y-4', 'opacity-0');
        toast.classList.add('translate-y-0', 'opacity-100');
    }, 10);

    // Auto remove after 3.5s
    setTimeout(() => {
        toast.classList.add('opacity-0', 'translate-y-2');
        setTimeout(() => toast.remove(), 300);
    }, 3500);
}

function addToCart(productId, quantity = 1) {
    const csrftoken = getCookie('csrftoken');
    const btn = document.getElementById(`add-btn-${productId}`);
    let originalHtml = '';
    if (btn) {
        originalHtml = btn.innerHTML;
        btn.innerHTML = `<i class="fa-solid fa-spinner fa-spin"></i> Adding...`;
        btn.disabled = true;
    }

    fetch('/shop/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
            'X-Requested-With': 'XMLHttpRequest',
        },
        body: JSON.stringify({
            product_id: productId,
            quantity: quantity,
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.status === 'success') {
            const badge = document.getElementById('cart-badge-count');
            if (badge) {
                badge.innerText = data.cart_count;
                badge.classList.add('scale-125');
                setTimeout(() => badge.classList.remove('scale-125'), 300);
            }
            showToastNotification(data.message || 'Product added to cart!');
            
            // If inventory is exhausted in cart
            if (data.remaining_stock === 0 && btn) {
                btn.disabled = true;
                btn.className = "w-full py-2.5 px-3 rounded-xl bg-slate-300 text-slate-500 font-bold text-xs cursor-not-allowed";
                btn.innerHTML = `<i class="fa-solid fa-check"></i> Added (Max in Cart)`;
                return;
            }
        } else {
            showToastNotification(data.message || 'Could not add product', 'error');
        }
    })
    .catch(err => {
        console.error(err);
        showToastNotification('Network error while adding to cart.', 'error');
    })
    .finally(() => {
        if (btn && !btn.disabled) {
            btn.innerHTML = originalHtml;
        }
    });
}
