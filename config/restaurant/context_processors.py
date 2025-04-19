from .models import Order

def cart_count(request):
    if request.user.is_authenticated:
        try:
            cart = Order.objects.get(user=request.user, status='pending')
            count = sum(item.quantity for item in cart.items.all())
            return {'cart_count': count}
        except Order.DoesNotExist:
            pass
    return {'cart_count': 0} 