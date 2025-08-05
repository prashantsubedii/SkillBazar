from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.db.models import Sum, Count
from .models import CustomUser
from .forms import ProfileUpdateForm, CustomPasswordChangeForm
from gigs.models import Gig, Order
from orders.models import Review


@login_required
def profile(request, username):
    user = get_object_or_404(CustomUser, username=username)
    user_gigs = Gig.objects.filter(freelancer=user, is_active=True)
    user_reviews = Review.objects.filter(freelancer=user).order_by('-created_at')[:5]
    
    context = {
        'profile_user': user,
        'user_gigs': user_gigs,
        'user_reviews': user_reviews,
    }
    return render(request, 'users/profile.html', context)


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile', username=request.user.username)
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'users/edit_profile.html', context)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = CustomPasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Password changed successfully!')
            return redirect('users:profile', username=request.user.username)
    else:
        form = CustomPasswordChangeForm(request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'users/change_password.html', context)


@login_required
def dashboard(request):
    user = request.user
    
    if user.user_type in ['freelancer', 'both']:
        # Freelancer dashboard
        my_gigs = Gig.objects.filter(freelancer=user)
        total_gigs = my_gigs.count()
        active_gigs = my_gigs.filter(is_active=True).count()
        
        # Orders received
        orders_received = Order.objects.filter(gig__freelancer=user)
        total_orders = orders_received.count()
        pending_orders = orders_received.filter(status='pending').count()
        completed_orders = orders_received.filter(status='completed').count()
        
        # Earnings
        total_earnings = orders_received.filter(status='completed').aggregate(
            total=Sum('amount')
        )['total'] or 0
        
        # Recent orders
        recent_orders = orders_received.order_by('-created_at')[:5]
        
        context = {
            'user_type': 'freelancer',
            'total_gigs': total_gigs,
            'active_gigs': active_gigs,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'completed_orders': completed_orders,
            'total_earnings': total_earnings,
            'recent_orders': recent_orders,
            'my_gigs': my_gigs[:5],
        }
    
    if user.user_type in ['buyer', 'both']:
        # Buyer dashboard
        my_orders = Order.objects.filter(buyer=user)
        total_orders_bought = my_orders.count()
        pending_orders_bought = my_orders.filter(status='pending').count()
        completed_orders_bought = my_orders.filter(status='completed').count()
        
        # Recent orders
        recent_orders_bought = my_orders.order_by('-created_at')[:5]
        
        if user.user_type == 'both':
            # Combine both dashboards
            context.update({
                'user_type': 'both',
                'total_orders_bought': total_orders_bought,
                'pending_orders_bought': pending_orders_bought,
                'completed_orders_bought': completed_orders_bought,
                'recent_orders_bought': recent_orders_bought,
            })
        else:
            context = {
                'user_type': 'buyer',
                'total_orders_bought': total_orders_bought,
                'pending_orders_bought': pending_orders_bought,
                'completed_orders_bought': completed_orders_bought,
                'recent_orders_bought': recent_orders_bought,
            }
    
    return render(request, 'users/dashboard.html', context) 