from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('home/', views.home, name='home'),
    path('login/',views.login,name='login'),
    path('vehicle_management/',views.vehicle_management,name='vehicle_management'),
    path('parking_status/',views.parking_status,name='parking_status'),
    path('vehicle_report/', views.vehicle_report, name='vehicle_report'),
]
