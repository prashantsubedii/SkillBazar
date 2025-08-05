from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.utils import timezone
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import timedelta
from decimal import Decimal
import requests
import json
import uuid
from .models import Review
from .forms import OrderForm, ReviewForm
from gigs.models import Gig, Order
from django.contrib.auth import get_user_model
from django.urls import reverse


@login_required
def create_order(request, gig_id):
    """Create a new order for a gig"""
    gig = get_object_or_404(Gig, id=gig_id, is_active=True)
    
    if request.user == gig.freelancer:
        messages.error(request, 'You cannot order your own gig!')
        return redirect('gigs:gig_detail', slug=gig.slug)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = Order.objects.create(
                    gig=gig,
                    buyer=request.user,
                    freelancer=gig.freelancer,
                    amount=gig.price,
                    requirements=form.cleaned_data['requirements']
                )
                messages.success(request, 'Order created successfully! Please complete your payment.')
                return redirect('orders:order_detail_with_payment', pk=order.pk)
    else:
        form = OrderForm()
    
    context = {
        'gig': gig,
        'form': form,
    }
    return render(request, 'orders/create_order.html', context)


@login_required
def create_order_and_pay(request, gig_id):
    """Create a new order and immediately open Khalti payment"""
    gig = get_object_or_404(Gig, id=gig_id, is_active=True)
    
    if request.user == gig.freelancer:
        messages.error(request, 'You cannot order your own gig!')
        return redirect('gigs:gig_detail', slug=gig.slug)
    
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                order = Order.objects.create(
                    gig=gig,
                    buyer=request.user,
                    freelancer=gig.freelancer,
                    amount=gig.price,
                    requirements=form.cleaned_data['requirements']
                )
                
                # Calculate payment details
                platform_fee = order.amount * Decimal('0.05')
                total_amount = order.amount + platform_fee
                
                # Khalti configuration
                khalti_config = {
                    'public_key': 'test_public_key_dc74c7d6d5134b94a2330cbbe3c57c54',
                    'product_identity': f"order_{order.id}",
                    'product_name': order.gig.title,
                    'amount': int(float(total_amount) * 100),  # Convert to paisa
                    'customer_info': {
                        'name': request.user.get_full_name() or request.user.username,
                        'email': request.user.email,
                        'phone': request.user.phone_number or "9800000000"
                    }
                }
                
                # Get the selected payment method from the form
                payment_method = request.POST.get('payment_method', 'khalti')
                
                context = {
                    'order': order,
                    'platform_fee': platform_fee,
                    'total_amount': total_amount,
                    'khalti_config': khalti_config,
                    'payment_method': payment_method,  # Pass the selected payment method
                    'auto_open': True,  # Flag to auto-open Khalti
                }
                return render(request, 'orders/direct_payment.html', context)
    else:
        form = OrderForm()
    
    # Calculate payment details for display
    platform_fee = gig.price * Decimal('0.05')
    total_amount = gig.price + platform_fee
    
    context = {
        'gig': gig,
        'form': form,
        'platform_fee': platform_fee,
        'total_amount': total_amount,
    }
    return render(request, 'orders/create_order.html', context)


@login_required
def order_detail_with_payment(request, pk):
    """Show order details with integrated Khalti payment"""
    order = get_object_or_404(Order, pk=pk)
    
    # Check if user has permission to view this order
    if request.user not in [order.buyer, order.freelancer]:
        messages.error(request, 'You do not have permission to view this order.')
        return redirect('gigs:home')
    
    # Check if user can leave a review
    can_review = (
        request.user == order.buyer and 
        order.status == 'completed' and
        not Review.objects.filter(gig=order.gig, reviewer=request.user).exists()
    )
    
    # Calculate payment details
    platform_fee = order.amount * Decimal('0.05')
    total_amount = order.amount + platform_fee
    
    # Khalti configuration
    khalti_config = {
        'public_key': 'test_public_key_dc74c7d6d5134b94a2330cbbe3c57c54',
        'product_identity': f"order_{order.id}",
        'product_name': order.gig.title,
        'amount': int(float(total_amount) * 100),  # Convert to paisa
        'customer_info': {
            'name': request.user.get_full_name() or request.user.username,
            'email': request.user.email,
            'phone': request.user.phone_number or "9800000000"
        }
    }
    
    context = {
        'order': order,
        'can_review': can_review,
        'platform_fee': platform_fee,
        'total_amount': total_amount,
        'khalti_config': khalti_config,
        'is_buyer': request.user == order.buyer,
    }
    return render(request, 'orders/order_detail_with_payment.html', context)


@login_required
def payment_integration(request, order_id):
    """Payment integration page with real Khalti and eSewa APIs"""
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    # Calculate fees
    platform_fee = order.amount * Decimal('0.05')  # 5% platform fee
    total_amount = order.amount + platform_fee
    
    # Generate unique transaction ID
    transaction_id = str(uuid.uuid4())
    
    # Khalti API Configuration (Test credentials)
    khalti_config = {
        'public_key': 'test_public_key_dc74c7d6d5134b94a2330cbbe3c57c54',
        'secret_key': 'test_secret_key_3e7b4c1d5f8a9b2c6d7e8f9a0b1c2d3e',
        'api_url': 'https://a.khalti.com/api/v2/epayment/initiate/',
        'verify_url': 'https://a.khalti.com/api/v2/epayment/lookup/',
    }
    
    # eSewa API Configuration (Test credentials)
    esewa_config = {
        'merchant_id': 'EPAYTEST',
        'api_url': 'https://esewa.com.np/epay/main',
        'verify_url': 'https://esewa.com.np/epay/transrec',
    }
    
    context = {
        'order': order,
        'platform_fee': platform_fee,
        'total_amount': total_amount,
        'transaction_id': transaction_id,
        'khalti_config': khalti_config,
        'esewa_config': esewa_config,
    }
    return render(request, 'orders/payment_integration.html', context)


@csrf_exempt
@require_POST
def khalti_payment_initiate(request):
    """Initiate Khalti payment"""
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        amount = data.get('amount')
        
        order = get_object_or_404(Order, id=order_id, buyer=request.user)
        
        # Khalti payment initiation
        khalti_data = {
            "public_key": "test_public_key_dc74c7d6d5134b94a2330cbbe3c57c54",
            "amount": int(float(amount) * 100),  # Convert to paisa
            "product_identity": f"order_{order_id}",
            "product_name": order.gig.title,
            "customer_info": {
                "name": request.user.get_full_name(),
                "email": request.user.email,
                "phone": request.user.phone_number or "9800000000"
            },
            "success_url": request.build_absolute_uri(f"/orders/payment-success/{order_id}/"),
            "failure_url": request.build_absolute_uri(f"/orders/payment-failure/{order_id}/"),
        }
        
        # In production, you would make a real API call to Khalti
        # For demo purposes, we'll simulate the response
        response_data = {
            "pidx": str(uuid.uuid4()),
            "payment_url": f"https://a.khalti.com/api/v2/epayment/initiate/?pidx={khalti_data['product_identity']}",
            "expires_at": "2024-12-31T23:59:59.999999Z"
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@csrf_exempt
@require_POST
def esewa_payment_initiate(request):
    """Initiate eSewa payment"""
    try:
        data = json.loads(request.body)
        order_id = data.get('order_id')
        amount = data.get('amount')
        
        order = get_object_or_404(Order, id=order_id, buyer=request.user)
        
        # eSewa payment initiation
        esewa_data = {
            "amt": amount,
            "pdc": 0,
            "psc": 0,
            "txAmt": 0,
            "tAmt": amount,
            "pid": f"order_{order_id}",
            "scd": "EPAYTEST",
            "su": request.build_absolute_uri(f"/orders/payment-success/{order_id}/"),
            "fu": request.build_absolute_uri(f"/orders/payment-failure/{order_id}/"),
        }
        
        # In production, you would redirect to eSewa
        # For demo purposes, we'll simulate the response
        response_data = {
            "payment_url": f"https://esewa.com.np/epay/main?pid={esewa_data['pid']}&amt={esewa_data['amt']}&tAmt={esewa_data['tAmt']}",
            "pid": esewa_data['pid']
        }
        
        return JsonResponse(response_data)
        
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)


@login_required
def payment_success(request, order_id):
    """Handle successful payment"""
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    # Update order status
    order.status = 'in_progress'
    order.save()
    
    messages.success(request, 'Payment successful! Your order has been placed.')
    return redirect('orders:order_detail', pk=order.pk)


@login_required
def payment_failure(request, order_id):
    """Handle failed payment"""
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    
    messages.error(request, 'Payment failed. Please try again.')
    return redirect('orders:payment_integration', order_id=order.pk)


@login_required
def order_detail(request, pk):
    """Show order details"""
    order = get_object_or_404(Order, pk=pk)
    
    # Check if user has permission to view this order
    if request.user not in [order.buyer, order.freelancer]:
        messages.error(request, 'You do not have permission to view this order.')
        return redirect('gigs:home')
    
    # Check if user can leave a review
    can_review = (
        request.user == order.buyer and 
        order.status == 'completed' and
        not Review.objects.filter(gig=order.gig, reviewer=request.user).exists()
    )
    
    # Calculate payment details
    platform_fee = order.amount * Decimal('0.05')
    total_amount = order.amount + platform_fee
    
    context = {
        'order': order,
        'can_review': can_review,
        'platform_fee': platform_fee,
        'total_amount': total_amount,
    }
    return render(request, 'orders/order_detail.html', context)


@login_required
def order_list(request):
    """Show user's orders"""
    if request.user.user_type in ['freelancer', 'both']:
        orders_received = Order.objects.filter(freelancer=request.user).order_by('-created_at')
    else:
        orders_received = []
    
    if request.user.user_type in ['buyer', 'both']:
        orders_bought = Order.objects.filter(buyer=request.user).order_by('-created_at')
    else:
        orders_bought = []
    
    context = {
        'orders_received': orders_received,
        'orders_bought': orders_bought,
    }
    return render(request, 'orders/order_list.html', context)


@login_required
def update_order_status(request, pk):
    """Update order status (freelancer only)"""
    order = get_object_or_404(Order, pk=pk, freelancer=request.user)
    
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in ['in_progress', 'completed', 'cancelled']:
            order.status = new_status
            if new_status == 'completed':
                order.delivery_date = timezone.now()
            order.save()
            messages.success(request, f'Order status updated to {new_status}.')
        else:
            messages.error(request, 'Invalid status.')
    
    return redirect('orders:order_detail', pk=order.pk)


@login_required
def submit_review(request, order_id):
    """Submit a review for a completed order"""
    order = get_object_or_404(Order, id=order_id, buyer=request.user, status='completed')
    
    # Check if review already exists
    if Review.objects.filter(gig=order.gig, reviewer=request.user).exists():
        messages.error(request, 'You have already reviewed this gig.')
        return redirect('orders:order_detail', pk=order.pk)
    
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.gig = order.gig
            review.reviewer = request.user
            review.freelancer = order.freelancer
            review.save()
            messages.success(request, 'Review submitted successfully!')
            return redirect('orders:order_detail', pk=order.pk)
    else:
        form = ReviewForm()
    
    context = {
        'form': form,
        'order': order,
    }
    return render(request, 'orders/submit_review.html', context) 


@login_required
def delete_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, buyer=request.user)
    if order.status == 'pending':
        order.delete()
        messages.success(request, 'Order cancelled successfully.')
    else:
        messages.error(request, 'Only pending orders can be cancelled.')
    return redirect(reverse('users:dashboard')) 