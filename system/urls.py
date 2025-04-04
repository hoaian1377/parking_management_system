from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'), 
    path('home/', views.home, name='home'),
    path('login/',views.login,name='login'),
    path('vehicle_entry',views.vehicle_entry,name='vehicle_entry'),
    path('parking_status',views.parking_status,name='parking_status'),
]