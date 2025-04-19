from django.shortcuts import render,redirect
from .models import Taikhoan
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth import logout


def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('tendangnhap')
        password = request.POST.get('matkhau')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)  # ✅ đây là chỗ dùng phần quản lý user mặc định
            return redirect('home')  # Đảm bảo bạn có url name là "home"
        else:
            return render(request, 'login.html', {
                'error': 'Sai tài khoản hoặc mật khẩu'
            })
    
    return render(request, 'login.html')



def home(request):
    return render(request,'home.html')
def register(request):
    return render(request,'register.html')
def vehicle_management(request):
    return render(request,'vehicle_management.html')
def parking_status(request):
    return render(request,'parking_status.html')
def vehicle_report(request):
    return render(request, 'vehicle_report.html')
def logout_view(request):
    logout(request)
    return redirect('login')



