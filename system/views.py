from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.contrib.auth.models import User
from .models import Xe, Vitridoxe, Nhanvien
import json
import uuid
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.decorators import login_required, permission_required

# ========================== VEHICLE MANAGEMENT ==========================

def vehicle_management(request):
    vehicles = Xe.objects.all()
    return render(request, 'vehicle_management.html', {'vehicles': vehicles})

@require_http_methods(["GET"])
def get_vehicles(request):
    try:
        vehicles = Xe.objects.all()
        data = []
        for vehicle in vehicles:
            vehicle_data = {
                'xeid': vehicle.xeid,
                'bienso': vehicle.bienso,
                'loaixe': vehicle.loaixe,
                'imgurl': vehicle.imgurl,
            }
            if vehicle.chuxe:
                vehicle_data['chuxe'] = {
                    'id': vehicle.chuxe.id,
                    'ten': getattr(vehicle.chuxe, 'ten', 'Không xác định')
                }
            data.append(vehicle_data)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
@transaction.atomic
def vehicle_entry(request):
    try:
        data = json.loads(request.body)
        bienso = data.get('bienso')
        thoigianvao = data.get('thoigianvao')
        vitri = data.get('vitri')

        if not bienso or not thoigianvao or not vitri:
            return JsonResponse({'error': 'Thiếu thông tin bắt buộc'}, status=400)

        xe = Xe.objects.filter(bienso=bienso).first()
        if not xe:
            xe = Xe(xeid=str(uuid.uuid4()), bienso=bienso, loaixe='Chưa xác định')
            xe.save()

        lich_su = LichSuXe(
            xeid=xe,
            thoigianvao=datetime.fromisoformat(thoigianvao.replace('Z', '+00:00')),
            vitri=vitri
        )
        lich_su.save()

        return JsonResponse({'status': 'success', 'message': 'Đã ghi nhận xe vào thành công', 'data': {
            'xeid': xe.xeid,
            'bienso': xe.bienso,
            'vitri': vitri
        }})
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@csrf_exempt
@require_http_methods(["POST"])
def vehicle_exit(request):
    try:
        data = json.loads(request.body)
        bienso = data.get('bienso')
        thoigianra = data.get('thoigianra')
        vitri = data.get('vitri')

        if not bienso or not thoigianra:
            return JsonResponse({'error': 'Thiếu thông tin bắt buộc'}, status=400)

        xe = Xe.objects.filter(bienso=bienso).first()
        if not xe:
            return JsonResponse({'error': 'Không tìm thấy xe trong hệ thống'}, status=404)

        lich_su = LichSuXe.objects.filter(xeid=xe, vitri=vitri, thoigianra__isnull=True).order_by('-thoigianvao').first()
        if not lich_su:
            return JsonResponse({'error': 'Không tìm thấy thông tin xe vào'}, status=404)

        lich_su.thoigianra = datetime.fromisoformat(thoigianra.replace('Z', '+00:00'))
        lich_su.save()

        return JsonResponse({
            'status': 'success',
            'message': 'Đã ghi nhận xe ra thành công',
            'data': {
                'xeid': xe.xeid,
                'bienso': xe.bienso,
                'vitri': vitri,
                'thoigianvao': lich_su.thoigianvao.isoformat(),
                'thoigianra': lich_su.thoigianra.isoformat()
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

# ========================== AUTH & VIEWS ==========================

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('tendangnhap')
        password = request.POST.get('matkhau')
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('home')
        return render(request, 'login.html', {'error': 'Sai tài khoản hoặc mật khẩu'})
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def home(request):
    return render(request, 'home.html')

def register(request):
    return render(request, 'register.html')

def parking_status(request):
    return render(request, 'parking_status.html')

def vehicle_report(request):
    return render(request, 'vehicle_report.html')

# ========================== PASSWORD RESET ==========================

def password_reset_request(request):
    if request.method == "POST":
        email = request.POST.get("email")
        users = User.objects.filter(email=email)
        if users.exists():
            user = users.first()
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            reset_link = request.build_absolute_uri(f"/reset/{uid}/{token}/")
            message = render_to_string("password_reset_email.html", {"user": user, "reset_link": reset_link})
            send_mail("Password Reset Requested", message, None, [email])
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
    return render(request, "password_reset_confirm.html", {"validlink": False})

# ========================== EMPLOYEE MANAGEMENT ==========================

@login_required
@permission_required('app.view_nhanvien', raise_exception=True)
def employee_management(request):
    nhanviens = Nhanvien.objects.all()
    return render(request, 'employee_management.html', {'nhanviens': nhanviens})
