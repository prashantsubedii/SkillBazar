from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils.text import slugify
from .models import Gig, Category, Order
from .forms import GigForm


def home(request):
    """Homepage view with featured gigs and categories"""
    categories = Category.objects.all()[:6]
    featured_gigs = Gig.objects.filter(is_active=True).order_by('-rating', '-views')[:8]
    recent_gigs = Gig.objects.filter(is_active=True).order_by('-created_at')[:6]
    
    context = {
        'categories': categories,
        'featured_gigs': featured_gigs,
        'recent_gigs': recent_gigs,
    }
    return render(request, 'gigs/home.html', context)


def gig_list(request):
    """List all gigs with filtering and search"""
    gigs = Gig.objects.filter(is_active=True)
    
    # Search functionality
    query = request.GET.get('q')
    if query:
        gigs = gigs.filter(
            Q(title__icontains=query) |
            Q(description__icontains=query) |
            Q(freelancer__username__icontains=query) |
            Q(category__name__icontains=query)
        )
    
    # Category filter
    category_slug = request.GET.get('category')
    if category_slug:
        gigs = gigs.filter(category__slug=category_slug)
    
    # Price filter
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')
    if min_price:
        gigs = gigs.filter(price__gte=min_price)
    if max_price:
        gigs = gigs.filter(price__lte=max_price)
    
    # Sort options
    sort = request.GET.get('sort', 'newest')
    if sort == 'price_low':
        gigs = gigs.order_by('price')
    elif sort == 'price_high':
        gigs = gigs.order_by('-price')
    elif sort == 'rating':
        gigs = gigs.order_by('-rating')
    else:  # newest
        gigs = gigs.order_by('-created_at')
    
    # Pagination
    paginator = Paginator(gigs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    categories = Category.objects.all()
    
    context = {
        'page_obj': page_obj,
        'categories': categories,
        'query': query,
        'category_slug': category_slug,
        'min_price': min_price,
        'max_price': max_price,
        'sort': sort,
    }
    return render(request, 'gigs/gig_list.html', context)


def gig_detail(request, slug):
    """Detail view for a specific gig"""
    gig = get_object_or_404(Gig, slug=slug, is_active=True)
    gig.increment_views()
    
    # Get related gigs
    related_gigs = Gig.objects.filter(
        category=gig.category,
        is_active=True
    ).exclude(id=gig.id)[:4]
    
    context = {
        'gig': gig,
        'related_gigs': related_gigs,
    }
    return render(request, 'gigs/gig_detail.html', context)


def category_gigs(request, slug):
    """Show gigs for a specific category"""
    category = get_object_or_404(Category, slug=slug)
    gigs = Gig.objects.filter(category=category, is_active=True).order_by('-created_at')
    
    # Pagination
    paginator = Paginator(gigs, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'category': category,
        'page_obj': page_obj,
    }
    return render(request, 'gigs/category_gigs.html', context)


@login_required
def create_gig(request):
    """Create a new gig"""
    if request.method == 'POST':
        form = GigForm(request.POST, request.FILES)
        if form.is_valid():
            gig = form.save(commit=False)
            gig.freelancer = request.user
            gig.slug = slugify(gig.title)
            gig.save()
            messages.success(request, 'Gig created successfully!')
            return redirect('gigs:gig_detail', slug=gig.slug)
    else:
        form = GigForm()
    
    context = {
        'form': form,
    }
    return render(request, 'gigs/create_gig.html', context)


@login_required
def edit_gig(request, slug):
    """Edit an existing gig"""
    gig = get_object_or_404(Gig, slug=slug, freelancer=request.user)
    
    if request.method == 'POST':
        form = GigForm(request.POST, request.FILES, instance=gig)
        if form.is_valid():
            gig = form.save()
            messages.success(request, 'Gig updated successfully!')
            return redirect('gigs:gig_detail', slug=gig.slug)
    else:
        form = GigForm(instance=gig)
    
    categories = Category.objects.all()
    
    context = {
        'form': form,
        'gig': gig,
        'categories': categories,
    }
    return render(request, 'gigs/edit_gig.html', context)


@login_required
def delete_gig(request, slug):
    """Delete a gig"""
    gig = get_object_or_404(Gig, slug=slug, freelancer=request.user)
    
    if request.method == 'POST':
        gig.delete()
        messages.success(request, 'Gig deleted successfully!')
        return redirect('users:dashboard')
    
    context = {
        'gig': gig,
    }
    return render(request, 'gigs/delete_gig.html', context)


@login_required
def my_gigs(request):
    """Show user's gigs"""
    gigs = Gig.objects.filter(freelancer=request.user).order_by('-created_at')
    
    context = {
        'gigs': gigs,
    }
    return render(request, 'gigs/my_gigs.html', context) 