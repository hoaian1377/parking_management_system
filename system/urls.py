from django.urls import path
from . import views
from .views import login_view

urlpatterns = [
    path('', login_view, name='login'), 
    path('home/', views.home, name='home'),
    path('vehicle_management/',views.vehicle_management,name='vehicle_management'),
    path('parking_status/',views.parking_status,name='parking_status'),
    path('vehicle_report/', views.vehicle_report, name='vehicle_report'),
    path('register/', views.register, name='register'),
    path('password_reset/', views.password_reset_request, name='password_reset'),
    path('reset/<uidb64>/<token>/', views.password_reset_confirm, name='password_reset_confirm'),
]