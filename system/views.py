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

# accounts/views.py
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib import messages

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        users = User.objects.filter(email=email)
        if users.exists():
            user = users[0]
            subject = "Password Reset Requested"
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = request.build_absolute_uri(f"/reset/{uid}/{token}/")
            message = render_to_string("password_reset_email.html", {
                "user": user,
                "reset_link": reset_link,
            })
            send_mail(subject, message, None, [email])
            messages.success(request, "Check your email for the reset link.")
        else:
            messages.error(request, "No user with that email exists.")
    return render(request, "password_reset.html")


def password_reset_confirm(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user and default_token_generator.check_token(user, token):
        if request.method == "POST":
            password = request.POST.get("password")
            user.set_password(password)
            user.save()
            messages.success(request, "Password has been reset.")
            return redirect("login")
        return render(request, "password_reset_confirm.html", {"validlink": True})
    else:
        return render(request, "password_reset_confirm.html", {"validlink": False})


