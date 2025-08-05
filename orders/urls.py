from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('create-order/<int:gig_id>/', views.create_order, name='create_order'),
    path('create-order-and-pay/<int:gig_id>/', views.create_order_and_pay, name='create_order_and_pay'),
    path('payment/<int:order_id>/', views.payment_integration, name='payment_integration'),
    path('khalti-payment/', views.khalti_payment_initiate, name='khalti_payment_initiate'),
    path('esewa-payment/', views.esewa_payment_initiate, name='esewa_payment_initiate'),
    path('payment-success/<int:order_id>/', views.payment_success, name='payment_success'),
    path('payment-failure/<int:order_id>/', views.payment_failure, name='payment_failure'),
    path('order/<int:pk>/', views.order_detail, name='order_detail'),
    path('order-with-payment/<int:pk>/', views.order_detail_with_payment, name='order_detail_with_payment'),
    path('orders/', views.order_list, name='order_list'),
    path('update-order-status/<int:pk>/', views.update_order_status, name='update_order_status'),
    path('submit-review/<int:order_id>/', views.submit_review, name='submit_review'),
    path('delete-order/<int:order_id>/', views.delete_order, name='delete_order'),
] 