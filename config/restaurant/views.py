from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .models import Reservation, MenuItem, Order, OrderItem, MenuItemOption
from .forms import SignUpForm
import re
from datetime import date, datetime, timedelta
from django.http import JsonResponse
from django.views.decorators.http import require_POST
import json
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from decimal import Decimal  # Add this import at the top
import stripe
from django.conf import settings
from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils import timezone

stripe.api_key = settings.STRIPE_SECRET_KEY

def create_default_menu_items():
    """Define default menu items with Indian Rupee prices"""
    default_items = [
        # Starters
        {
            "name": "Classic Bruschetta",
            "price": 299.00,
            "description": "Toasted bread topped with fresh tomatoes, basil, and extra virgin olive oil",
            "image": "https://images.unsplash.com/photo-1506280754576-f6fa8a873550?w=800&q=80",
            "category": "starters",
        },
        {
            "name": "Crispy Calamari",
            "price": 399.00,
            "description": "Lightly fried squid rings served with lemon aioli",
            "image": "https://images.unsplash.com/photo-1604909052743-94e838986d24?w=800&q=80",
            "category": "starters",
        },
        {
            "name": "Stuffed Mushrooms",
            "price": 349.00,
            "description": "Mushrooms stuffed with cheese and herbs",
            "image": "https://images.unsplash.com/photo-1611599538835-b52a8c2af7fe?w=800&q=80",
            "category": "starters",
        },

        # Mains
        {
            "name": "Grilled Ribeye Steak",
            "price": 1299.00,
            "description": "12oz prime ribeye with roasted garlic butter and seasonal vegetables",
            "image": "https://images.unsplash.com/photo-1546964124-0cce460f38ef?w=800&q=80",
            "category": "mains",
        },
        {
            "name": "Herb Roasted Chicken",
            "price": 699.00,
            "description": "Free-range chicken with herbs, roasted potatoes, and natural jus",
            "image": "https://images.unsplash.com/photo-1604908176997-125f25cc6f3d?w=800&q=80",
            "category": "mains",
        },
        {
            "name": "Margherita Pizza",
            "price": 449.00,
            "description": "Classic pizza with fresh tomatoes, mozzarella, basil, and olive oil",
            "image": "https://images.unsplash.com/photo-1604068549290-dea0e4a305ca?w=800&q=80",
            "category": "mains",
        },

        # Seafood
        {
            "name": "Pan-Seared Sea Bass",
            "price": 1199.00,
            "description": "Fresh sea bass fillet with crispy skin, served with saffron risotto and asparagus",
            "image": "https://images.unsplash.com/photo-1615141982883-c7ad0e69fd62?w=800&q=80",
            "category": "seafood",
        },
        {
            "name": "Grilled Octopus",
            "price": 899.00,
            "description": "Tender octopus marinated in herbs and olive oil, served with roasted potatoes",
            "image": "https://images.unsplash.com/photo-1585545335512-1e43f40d4999?w=800&q=80",
            "category": "seafood",
        },
        {
            "name": "Seafood Paella",
            "price": 1299.00,
            "description": "Spanish rice with mixed seafood, saffron, and seasonal vegetables",
            "image": "https://images.unsplash.com/photo-1534080564583-6be75777b70a?w=800&q=80",
            "category": "seafood",
        },
        {
            "name": "Tuna Tartare",
            "price": 799.00,
            "description": "Fresh tuna diced and seasoned, served with avocado and crispy wontons",
            "image": "https://images.unsplash.com/photo-1626645738196-c2a7c87a8f58?w=800&q=80",
            "category": "seafood",
        },

        # Desserts
        {
            "name": "Chocolate Lava Cake",
            "price": 299.00,
            "description": "Warm chocolate cake with molten center and vanilla ice cream",
            "image": "https://images.unsplash.com/photo-1624353365286-3f8d62daad51?w=800&q=80",
            "category": "desserts",
        },
        {
            "name": "Tiramisu",
            "price": 349.00,
            "description": "Classic Italian dessert with coffee-soaked ladyfingers and mascarpone",
            "image": "https://images.unsplash.com/photo-1571877227200-a0d98ea607e9?w=800&q=80",
            "category": "desserts",
        },
        {
            "name": "Crème Brûlée",
            "price": 299.00,
            "description": "Rich vanilla custard with caramelized sugar crust",
            "image": "https://images.unsplash.com/photo-1470124182917-cc6e71b22ecc?w=800&q=80",
            "category": "desserts",
        },
    ]

    # Create menu items if they don't exist
    for item in default_items:
        MenuItem.objects.get_or_create(
            name=item["name"],
            defaults={
                "description": item["description"],
                "price": item["price"],
                "image": item["image"],
                "category": item["category"],
            }
        )

def home(request):
    """
    Renders your single-page front-end with dynamic menu items.
    """
    # Seed the database with default menu items if they don't exist.
    create_default_menu_items()
    
    # Query the menu items to pass to the template.
    starters = MenuItem.objects.filter(category='starters')
    mains = MenuItem.objects.filter(category='mains')
    seafood = MenuItem.objects.filter(category='seafood')
    desserts = MenuItem.objects.filter(category='desserts')
    context = {
        'starters': starters,
        'mains': mains,
        'seafood': seafood,
        'desserts': desserts,
    }
    return render(request, 'restaurant/index.html', context)

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            # Create the user
            user = User.objects.create_user(
                username=form.cleaned_data['username'],
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password'],
            )
            messages.success(request, "Account created! Please login.")
            return redirect('login')
        else:
            return render(
                request,
                'restaurant/index.html',
                {
                    'signup_form': form,
                    'show_signup_modal': True,
                }
            )
    else:
        form = SignUpForm()
        return render(
            request,
            'restaurant/index.html',
            {
                'signup_form': form,
                'show_signup_modal': True,
            }
        )

def login_view(request):
    if request.method == 'POST':
        username_or_email = request.POST.get('username')
        password = request.POST.get('password')

        # Try username first
        user = authenticate(request, username=username_or_email, password=password)
        if not user:
            # Try email
            try:
                possible_user = User.objects.get(email=username_or_email)
                user = authenticate(request, username=possible_user.username, password=password)
            except User.DoesNotExist:
                user = None

        if user:
            login(request, user)
            messages.success(request, "You are now logged in!")
            return redirect('home')
        else:
            messages.error(request, "Invalid credentials or user does not exist.")
            return redirect('login')

    return render(request, 'restaurant/index.html')

def logout_view(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('home')

@login_required
def book_table(request):
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        date = request.POST.get('date')
        time = request.POST.get('time')
        guests = request.POST.get('guests')
        special_requests = request.POST.get('special_requests')

        # Create reservation and associate it with the current user
        reservation = Reservation.objects.create(
            user=request.user,  # Associate with current user
            name=name,
            phone=phone,
            date=date,
            time=time,
            guests=guests,
            special_requests=special_requests
        )

        messages.success(request, 'Your reservation has been confirmed!')
        return redirect('my_reservations')

    return render(request, 'restaurant/index.html')

@login_required
def my_reservations(request):
    # Get only the reservations for the logged-in user
    reservations = Reservation.objects.filter(user=request.user).order_by('-date', '-time')
    
    context = {
        'reservations': reservations,
        'today_date': date.today(),
    }
    return render(request, 'restaurant/my_reservations.html', context)

@login_required
def modify_reservation(request, reservation_id):
    # Get the reservation object or return 404
    reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
    
    if request.method == 'POST':
        # Get form data
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        date_str = request.POST.get('date')
        time_str = request.POST.get('time')
        guests = request.POST.get('guests')
        special_requests = request.POST.get('special_requests')

        try:
            # Convert date string to date object
            reservation_date = datetime.strptime(date_str, '%Y-%m-%d').date()
            # Convert time string to time object
            reservation_time = datetime.strptime(time_str, '%H:%M').time()

            # Update reservation
            reservation.name = name
            reservation.phone = phone
            reservation.date = reservation_date
            reservation.time = reservation_time
            reservation.guests = guests
            reservation.special_requests = special_requests
            reservation.save()

            messages.success(request, 'Reservation updated successfully!')
            return redirect('my_reservations')
        except ValueError as e:
            messages.error(request, 'Invalid date or time format')
            return redirect('my_reservations')

    # For GET request
    context = {
        'reservation': reservation,
        'today_date': date.today(),
    }
    return render(request, 'restaurant/modify_reservation.html', context)

@login_required
def cancel_reservation(request, reservation_id):
    if request.method == 'POST':
        reservation = get_object_or_404(Reservation, id=reservation_id, user=request.user)
        
        # Only allow cancellation of future reservations
        if reservation.date >= date.today():
            reservation.delete()
            messages.success(request, 'Reservation cancelled successfully!')
        else:
            messages.error(request, 'Cannot cancel past reservations!')
        
        return redirect('my_reservations')
    
    return redirect('my_reservations')

def online_order(request):
    """Display the online ordering page"""
    menu_items = MenuItem.objects.all().prefetch_related('options')
    menu_by_category = {}
    
    for item in menu_items:
        if item.category not in menu_by_category:
            menu_by_category[item.category] = []
        menu_by_category[item.category].append({
            'id': item.id,
            'name': item.name,
            'description': item.description,
            'price': item.price,
            'image': item.image,
            'options': list(item.options.all())
        })

    # Calculate tax and total if there's a cart
    try:
        if request.user.is_authenticated:
            cart = Order.objects.get(user=request.user, status='pending')
            tax_rate = Decimal('0.08')  # 8% tax
            tax_amount = cart.total_amount * tax_rate
            total_with_tax = cart.total_amount + tax_amount
        else:
            cart = None
            tax_amount = Decimal('0.00')
            total_with_tax = Decimal('0.00')
    except Order.DoesNotExist:
        cart = None
        tax_amount = Decimal('0.00')
        total_with_tax = Decimal('0.00')

    context = {
        'menu_by_category': menu_by_category,
        'cart': cart,
        'tax_amount': tax_amount,
        'total_with_tax': total_with_tax,
    }
    
    return render(request, 'restaurant/online_order.html', context)

@ensure_csrf_cookie
@require_POST
def add_to_cart(request):
    """Add an item to the cart"""
    if not request.user.is_authenticated:
        return JsonResponse({
            'success': False,
            'message': 'Please login to add items to your cart',
            'require_login': True
        }, status=401)
    
    try:
        data = json.loads(request.body)
        menu_item_id = data.get('menu_item_id')
        quantity = int(data.get('quantity', 1))
        selected_options = data.get('options', {})
        
        # Validate menu item exists
        menu_item = MenuItem.objects.get(id=menu_item_id)
        
        # Get or create cart (Order with pending status)
        cart, created = Order.objects.get_or_create(
            user=request.user,
            status='pending',
            defaults={
                'total_amount': Decimal('0.00'),
                'pickup_time': datetime.now() + timedelta(hours=1)
            }
        )
        
        # Create or update order item
        order_item, created = OrderItem.objects.get_or_create(
            order=cart,
            menu_item=menu_item,
            defaults={
                'quantity': quantity,
                'selected_options': selected_options,
                'item_total': Decimal('0.00')  # Will be calculated in save()
            }
        )
        
        if not created:
            order_item.quantity += quantity
            order_item.selected_options.update(selected_options)
        
        order_item.save()
        
        # Update order total
        cart.total_amount = sum(item.item_total for item in cart.items.all())
        cart.save()
        
        return JsonResponse({
            'status': 'success',
            'message': 'Item added to cart',
            'cart_total': str(cart.total_amount),
            'cart_count': cart.items.count()
        })
        
    except MenuItem.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Menu item not found'
        }, status=404)
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@login_required
def view_cart(request):
    """View the current cart"""
    try:
        cart = Order.objects.get(user=request.user, status='pending')
        cart_items = cart.items.all().select_related('menu_item')
        
        # Calculate GST and total using Decimal
        tax_rate = Decimal('0.18')  # 18% GST
        tax_amount = cart.total_amount * tax_rate
        total_with_tax = cart.total_amount + tax_amount
        
        # Set pickup time to 30 minutes from now using timezone-aware datetime
        current_time = timezone.localtime(timezone.now())
        pickup_time = current_time + timedelta(minutes=30)
        
        # Ensure pickup time is within business hours (11 AM to 9 PM)
        opening_time = timezone.make_aware(datetime.combine(current_time.date(), 
                                         datetime.strptime('11:00', '%H:%M').time()))
        closing_time = timezone.make_aware(datetime.combine(current_time.date(), 
                                         datetime.strptime('21:00', '%H:%M').time()))
        
        if pickup_time < opening_time:
            pickup_time = opening_time
        elif pickup_time > closing_time:
            messages.warning(request, 'Restaurant is closed for today. Your order will be scheduled for tomorrow at 11 AM.')
            next_day = current_time.date() + timedelta(days=1)
            pickup_time = timezone.make_aware(datetime.combine(next_day, 
                                            datetime.strptime('11:00', '%H:%M').time()))
        
    except Order.DoesNotExist:
        cart = None
        cart_items = []
        tax_amount = Decimal('0.00')
        total_with_tax = Decimal('0.00')
        pickup_time = None

    context = {
        'cart': cart,
        'cart_items': cart_items,
        'tax_amount': tax_amount,
        'total_with_tax': total_with_tax,
        'pickup_time': pickup_time,
    }
    
    return render(request, 'restaurant/cart.html', context)

@require_POST
@login_required
def update_cart(request):
    """Update cart item quantities or remove items"""
    data = json.loads(request.body)
    item_id = data.get('item_id')
    quantity = data.get('quantity', 0)
    
    try:
        order_item = OrderItem.objects.get(
            id=item_id,
            order__user=request.user,
            order__status='pending'
        )
        
        if quantity > 0:
            order_item.quantity = quantity
            order_item.save()
        else:
            order_item.delete()
            
        # Update order total
        order = order_item.order
        order.total_amount = sum(item.item_total for item in order.items.all())
        order.save()
        
        return JsonResponse({
            'status': 'success',
            'cart_total': str(order.total_amount)
        })
        
    except OrderItem.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Item not found'
        }, status=404)

@login_required
def cart_preview(request):
    """Return cart data for the floating preview"""
    try:
        cart = Order.objects.get(user=request.user, status='pending')
        items = [{
            'name': item.menu_item.name,
            'quantity': item.quantity,
            'total': str(item.item_total)  # Convert Decimal to string
        } for item in cart.items.all()]
        
        return JsonResponse({
            'items': items,
            'total': str(cart.total_amount)  # Convert Decimal to string
        })
    except Order.DoesNotExist:
        return JsonResponse({
            'items': [],
            'total': '0.00'
        })

@login_required
def checkout(request):
    """Process checkout"""
    if request.method == 'POST':
        try:
            cart = Order.objects.get(user=request.user, status='pending')
            
            # Get form data
            pickup_time = request.POST.get('pickup_time')
            special_instructions = request.POST.get('special_instructions')
            
            # Convert pickup time to timezone-aware datetime
            pickup_datetime = datetime.strptime(pickup_time, '%Y-%m-%d %H:%M')
            pickup_time_aware = timezone.make_aware(pickup_datetime)
            
            # Update order
            cart.pickup_time = pickup_time_aware
            cart.special_instructions = special_instructions
            cart.status = 'confirmed'
            cart.save()
            
            messages.success(request, 'Order placed successfully!')
            return redirect('order_confirmation', order_id=cart.id)
            
        except Order.DoesNotExist:
            messages.error(request, 'No active cart found.')
            return redirect('online_order')
        except Exception as e:
            messages.error(request, f'Error processing order. Please try again.')
            print(f"Checkout error: {str(e)}")
            return redirect('view_cart')
    
    return redirect('view_cart')

@login_required
def order_confirmation(request, order_id):
    """Display order confirmation page"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    context = {
        'order': order,
        'items': order.items.all().select_related('menu_item')
    }
    return render(request, 'restaurant/order_confirmation.html', context)

@login_required
def order_history(request):
    """Display user's order history"""
    orders = Order.objects.filter(
        user=request.user
    ).exclude(
        status='pending'
    ).order_by('-created_at')

    context = {
        'orders': orders
    }
    return render(request, 'restaurant/order_history.html', context)

@login_required
def track_order(request, order_id):
    """Track specific order"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Get order timeline
    timeline = []
    
    # Order Placed
    timeline.append({
        'status': 'Order Placed',
        'time': order.created_at,
        'completed': True
    })
    
    # Order Confirmed
    timeline.append({
        'status': 'Order Confirmed',
        'time': order.confirmed_at,
        'completed': bool(order.confirmed_at)
    })
    
    # Preparing
    timeline.append({
        'status': 'Preparing',
        'time': order.preparing_at,
        'completed': bool(order.preparing_at)
    })
    
    # Ready for Pickup
    timeline.append({
        'status': 'Ready for Pickup',
        'time': order.ready_at,
        'completed': bool(order.ready_at)
    })
    
    # Completed
    timeline.append({
        'status': 'Completed',
        'time': order.completed_at,
        'completed': bool(order.completed_at)
    })
    
    context = {
        'order': order,
        'timeline': timeline
    }
    return render(request, 'restaurant/track_order.html', context)

@login_required
def toggle_favorite_order(request, order_id):
    """Toggle order as favorite"""
    order = get_object_or_404(Order, id=order_id, user=request.user)
    order.is_favorite = not order.is_favorite
    order.save()
    return JsonResponse({'status': 'success', 'is_favorite': order.is_favorite})

@login_required
def reorder(request, order_id):
    """Create a new order based on a previous order"""
    old_order = get_object_or_404(Order, id=order_id, user=request.user)
    
    # Create new cart with current time + 30 minutes for pickup
    pickup_time = timezone.localtime(timezone.now() + timedelta(minutes=30))
    
    new_order = Order.objects.create(
        user=request.user,
        status='pending',
        total_amount=Decimal('0.00'),
        pickup_time=pickup_time
    )
    
    # Copy items from old order
    for item in old_order.items.all():
        OrderItem.objects.create(
            order=new_order,
            menu_item=item.menu_item,
            quantity=item.quantity,
            selected_options=item.selected_options,
            item_total=item.item_total
        )
    
    # Update total
    new_order.total_amount = sum(item.item_total for item in new_order.items.all())
    new_order.save()
    
    messages.success(request, 'Items added to cart!')
    return redirect('view_cart')

@login_required
def create_payment_intent(request, order_id):
    """Create a payment intent for Stripe"""
    try:
        order = Order.objects.get(id=order_id, user=request.user)
        
        # Create a PaymentIntent with the order amount and currency
        intent = stripe.PaymentIntent.create(
            amount=int(order.get_total_with_tax() * 100),
            currency='inr',  # Changed to Indian Rupees
            metadata={
                'order_id': order.id,
                'user_id': request.user.id
            }
        )
        
        order.stripe_payment_intent = intent.id
        order.save()
        
        return JsonResponse({
            'clientSecret': intent.client_secret,
            'publicKey': settings.STRIPE_PUBLISHABLE_KEY
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=403)

@require_POST
def stripe_webhook(request):
    """Handle Stripe webhooks"""
    try:
        event = stripe.Webhook.construct_event(
            request.body, request.META['HTTP_STRIPE_SIGNATURE'], 
            settings.STRIPE_WEBHOOK_SECRET
        )

        if event.type == 'payment_intent.succeeded':
            payment_intent = event.data.object
            order_id = payment_intent.metadata.get('order_id')
            
            # Update order status
            order = Order.objects.get(id=order_id)
            order.payment_status = 'paid'
            order.update_status('confirmed')  # Use the new method
            
            # Send confirmation email
            send_order_confirmation(order)
            
        return JsonResponse({'status': 'success'})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

@login_required
def update_order_status(request, order_id):
    """Update order status (for staff/admin)"""
    if not request.user.is_staff:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
        
    try:
        order = Order.objects.get(id=order_id)
        new_status = request.POST.get('status')
        
        if new_status in ['confirmed', 'preparing', 'ready', 'completed']:
            order.update_status(new_status)
            return JsonResponse({'status': 'success'})
        else:
            return JsonResponse({'error': 'Invalid status'}, status=400)
            
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)

def order_status_api(request, order_id):
    try:
        order = Order.objects.get(id=order_id)
        return JsonResponse({
            'status': order.status,
            'confirmed_at': order.confirmed_at.isoformat() if order.confirmed_at else None,
            'preparing_at': order.preparing_at.isoformat() if order.preparing_at else None,
            'ready_at': order.ready_at.isoformat() if order.ready_at else None,
            'completed_at': order.completed_at.isoformat() if order.completed_at else None,
        })
    except Order.DoesNotExist:
        return JsonResponse({'error': 'Order not found'}, status=404)
