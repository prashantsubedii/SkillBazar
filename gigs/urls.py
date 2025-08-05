from django.urls import path
from . import views

app_name = 'gigs'

urlpatterns = [
    path('', views.home, name='home'),
    path('gigs/', views.gig_list, name='gig_list'),
    path('gig/<slug:slug>/', views.gig_detail, name='gig_detail'),
    path('category/<slug:slug>/', views.category_gigs, name='category'),
    path('create-gig/', views.create_gig, name='create_gig'),
    path('edit-gig/<slug:slug>/', views.edit_gig, name='edit_gig'),
    path('delete-gig/<slug:slug>/', views.delete_gig, name='delete_gig'),
    path('my-gigs/', views.my_gigs, name='my_gigs'),
] 