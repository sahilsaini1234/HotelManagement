# bookings/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('bookings/create/', views.create_booking, name='create_booking'),
    path('bookings/edit/<int:booking_id>/', views.edit_booking, name='edit_booking'),
    path('bookings/cancel/<int:booking_id>/', views.cancel_booking, name='cancel_booking'),
    path('bookings/view/', views.view_bookings, name='view_bookings'),
]
