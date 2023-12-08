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
    path('booking/', views.booking , name='booking'),
]