from .views import machine_details
from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('create_customer/', views.create_customer, name='create_customer'),
    path('customer_list/', views.customer_list, name='customer_list'),
    path('machine_list/', views.machine_list, name='machine_list'),
    path('reports/', views.reports, name='generate_reports'),
    path('update_customer_details/<customer_id>/', views.update_customer_details, name='update_customer'),
    path('machines/', views.machine_list, name='machine_list'),
    path('create_machine/', views.create_machine, name='create_machine'),
    path('create_booking/', views.create_booking, name='create_booking'),
    path('view_bookings/', views.view_bookings, name='view_bookings'),
    path('update_booking/<str:booking_id>/',views.update_booking, name='update_booking'),
    path('machine_details/<str:machine_name>/', views.machine_details, name='machine_details'),
]
