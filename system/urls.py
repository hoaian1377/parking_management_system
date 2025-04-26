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
    path('home/employee_management/', views.employee_management, name='employee_management'),
    path('employee/delete/<str:nhanvienid>/', views.delete_employee, name='delete_employee'),
    path('employee-management/', views.employee_management, name='employee_management'),
    path('employee_management/', views.employee_management, name='employee_management'),
    path('add_employee/', views.add_employee, name='add_employee'),
    path('nhanvien/', views.employee_management, name='employee_management'),
    path('nhanvien/sua/<str:nhanvienid>/', views.edit_employee, name='edit_employee'),
    path('nhanvien/xoa/<str:nhanvienid>/', views.delete_employee, name='delete_employee'),
    path('nhanvien/them/', views.add_employee, name='add_employee'),
    path('search/', views.search_employee, name='search_employee'),
    path('vehicles/', views.vehicle_management, name='vehicle_management'),  # Trang danh sách xe
    path('vehicle/edit/<str:pk>/', views.vehicle_edit, name='vehicle_edit'),  # Trang sửa xe
    path('vehicle/delete/<str:pk>/', views.vehicle_delete, name='vehicle_delete'),  # Trang xóa xe
    path('vehicle_report/export/', views.export_vehicle_report, name='export_vehicle_report'),  # Xuất báo cáo xe
]