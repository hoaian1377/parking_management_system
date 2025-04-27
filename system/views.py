from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.db import transaction
from django.contrib.auth.models import User
from .models import Xe, Vitridoxe, Luotravao, Giave
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
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.db import transaction
from django.template.loader import render_to_string
from django.utils.dateparse import parse_date
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.db import transaction
from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render
from .models import Nhanvien
import xlwt
from django.contrib.auth.models import User
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import redirect

# ========================== VEHICLE MANAGEMENT =========================


from django.contrib.auth.models import User

def add_employee(request):
    if request.method == 'POST':
        nhanvienid = request.POST.get('nhanvienid')
        hoten = request.POST.get('hoten')
        chucvu = request.POST.get('chucvu')  # Chức vụ có thể quyết định quyền
        phanquyen = request.POST.get('phanquyen')
        diachi = request.POST.get('diachi')
        sodienthoai = request.POST.get('sodienthoai')
        ngaysinh = request.POST.get('ngaysinh')
        email = request.POST.get('email')
        matkhau = request.POST.get('matkhau')

        # Kiểm tra mã nhân viên đã tồn tại trong bảng Nhanvien
        if Nhanvien.objects.filter(nhanvienid=nhanvienid).exists():
            messages.error(request, "Mã nhân viên đã tồn tại.")
            return redirect('employee_management')

        # Kiểm tra tài khoản User đã tồn tại chưa
        if User.objects.filter(username=nhanvienid).exists():
            messages.error(request, "Tài khoản đăng nhập đã tồn tại.")
            return redirect('employee_management')

        try:
            # Thêm vào bảng Nhanvien
            Nhanvien.objects.create(
                nhanvienid=nhanvienid,
                hoten=hoten,
                chucvu=chucvu,
                phanquyen=phanquyen,
                diachi=diachi,
                sodienthoai=sodienthoai,
                ngaysinh=ngaysinh,
                email=email,
                matkhau=matkhau
            )

            # Tạo tài khoản User để đăng nhập
            user = User.objects.create_user(
                username=nhanvienid,     # username là mã nhân viên
                password=matkhau,         # mật khẩu nhân viên nhập
                email=email,
                first_name=hoten
            )

            # Cấp quyền cho tài khoản User
            if chucvu == 'Quản lý':
                user.is_staff = True
                user.is_superuser = True  # Quản lý có quyền superuser
            else:
                user.is_staff = True  # Nhân viên có quyền staff

            # Lưu lại quyền cho user
            user.save()

            messages.success(request, "Thêm nhân viên và tài khoản đăng nhập thành công.")
        except Exception as e:
            messages.error(request, f"Lỗi khi thêm nhân viên: {e}")

    return redirect('employee_management')




# ========================== VEHICLE MANAGEMENT ==========================

from django.shortcuts import render

def search_employee(request):
    query = request.GET.get('nhanvienid')
    nhanvien = Nhanvien.objects.filter(nhanvienid=query)
    return render(request, 'employee_management.html', {'nhanviens': nhanvien, 'query': query})


def add_employee(request):
    if request.method == 'POST':
        nhanvienid = request.POST.get('nhanvienid')
        hoten = request.POST.get('hoten')
        chucvu = request.POST.get('chucvu')
        phanquyen = request.POST.get('phanquyen')
        diachi = request.POST.get('diachi')
        sodienthoai = request.POST.get('sodienthoai')
        ngaysinh=request.POST.get('ngaysinh')
        email=request.POST.get('email')
        matkhau=request.POST.get('matkhau')


        # Kiểm tra mã nhân viên đã tồn tại chưa
        if Nhanvien.objects.filter(nhanvienid=nhanvienid).exists():
            messages.error(request, "Mã nhân viên đã tồn tại.")
            return redirect('employee_management')

        # Thêm nhân viên mới
        try:
            Nhanvien.objects.create(
                nhanvienid=nhanvienid,
                hoten=hoten,
                chucvu=chucvu,
                phanquyen=phanquyen,
                diachi=diachi,
                sodienthoai=sodienthoai,
                ngaysinh=ngaysinh,
                email=email,
                matkhau=matkhau
            )
            messages.success(request, "Thêm nhân viên thành công.")
        except Exception as e:
            messages.error(request, f"Lỗi khi thêm nhân viên: {e}")

    return redirect('employee_management')



# View quản lý nhân viên, hiển thị danh sách nhân viên
def employee_management(request):
    employees = Nhanvien.objects.all()  # Lấy danh sách tất cả nhân viên
    return render(request, 'employee_management.html', {'nhanvien': employees})


# Employee Management Views

@login_required
@permission_required('app.view_nhanvien', raise_exception=True)
def employee_management(request):
    nhanviens = Nhanvien.objects.all()
    return render(request, 'employee_management.html', {'nhanviens': nhanviens})

# Edit Employee
@login_required
@permission_required('app.change_nhanvien', raise_exception=True)
def edit_employee(request, nhanvienid):
    employee = get_object_or_404(Nhanvien, nhanvienid=nhanvienid)

    if request.method == "POST":
        try:
            employee.hoten = request.POST.get('hoten')
            employee.chucvu = request.POST.get('chucvu')
            employee.phanquyen = request.POST.get('phanquyen')
            employee.diachi = request.POST.get('diachi')
            employee.sodienthoai = request.POST.get('sodienthoai')
            employee.ngaysinh = request.POST.get('ngaysinh')
            employee.email = request.POST.get('email')
            employee.matkhau = request.POST.get('matkhau')
            

            employee.save()

            messages.success(request, "Thông tin nhân viên đã được cập nhật.")
            return redirect('employee_management')
        except Exception as e:
            messages.error(request, f"Đã có lỗi xảy ra: {str(e)}")
            return redirect('employee_management')

    return render(request, 'edit_employee.html', {'employee': employee})

# Delete Employee
@login_required
@permission_required('app.delete_nhanvien', raise_exception=True)
def delete_employee(request, nhanvienid):
    try:
        employee = get_object_or_404(Nhanvien, nhanvienid=nhanvienid)
        employee.delete()
        messages.success(request, "Nhân viên đã được xóa thành công.")
    except Exception as e:
        messages.error(request, f"Đã có lỗi xảy ra: {str(e)}")
    
    return redirect('employee_management')

# Search Employees



@login_required
@permission_required('app.view_nhanvien', raise_exception=True)
def employee_management(request):
    nhanviens = Nhanvien.objects.all()
    return render(request, 'employee_management.html', {'nhanviens': nhanviens})

def vehicle_management(request):
    vehicles = Xe.objects.all()
    return render(request, 'vehicle_management.html', {'vehicles': vehicles})


# API - Danh sách xe
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
                'chuxe': {
                    'id': vehicle.chuxe.id,
                    'ten': getattr(vehicle.chuxe, 'ten', 'Không xác định')
                } if vehicle.chuxe else None
            }
            data.append(vehicle_data)
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)

@require_http_methods(["GET"])
def search_vehicles(request):
    try:
        query = request.GET.get('q', '').strip().lower()
        if not query:
            return JsonResponse([], safe=False)
        vehicles = Xe.objects.filter(
            models.Q(bienso__icontains=query) |
            models.Q(loaixe__icontains=query) |
            models.Q(xeid__icontains=query)
        )
        data = [{
            'xeid': v.xeid,
            'bienso': v.bienso,
            'loaixe': v.loaixe,
            'imgurl': v.imgurl,
            'chuxe': {
                'id': v.chuxe.id,
                'ten': getattr(v.chuxe, 'ten', 'Không xác định')
            } if v.chuxe else None
        } for v in vehicles]
        return JsonResponse(data, safe=False)
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# API - Ghi nhận xe vào
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

        xe, created = Xe.objects.get_or_create(
            bienso=bienso,
            defaults={'xeid': str(uuid.uuid4()), 'loaixe': 'Chưa xác định'}
        )

        LichSuXe.objects.create(
            xeid=xe,
            thoigianvao=datetime.fromisoformat(thoigianvao.replace('Z', '+00:00')),
            vitri=vitri
        )

        return JsonResponse({
            'status': 'success',
            'message': 'Đã ghi nhận xe vào thành công',
            'data': {
                'xeid': xe.xeid,
                'bienso': xe.bienso,
                'vitri': vitri
            }
        })
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=500)


# API - Ghi nhận xe ra
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

        lich_su = LichSuXe.objects.filter(
            xeid=xe,
            vitri=vitri,
            thoigianra__isnull=True
        ).order_by('-thoigianvao').first()

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

def vehicle_management(request):
    vehicles = Xe.objects.all()

    # Nếu có yêu cầu POST để thêm xe vào, gán A1 nếu trống
    if request.method == 'POST':
        bienso = request.POST.get('bienso')
        thoigianvao = request.POST.get('thoigianvao')
        if not Xe.objects.filter(bienso=bienso, thoigianra__isnull=True).exists():
            xe = Xe(
                xeid=f"{bienso}-{timezone.now().timestamp()}",
                bienso=bienso,
                thoigianvao=thoigianvao,
            )
            xe.save()
        return redirect('vehicle_management')

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
    try:
        # Get filter parameters from request
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        vehicle_type = request.GET.get('vehicle_type', 'all')
        
        # Base query
        parking_records = Luotravao.objects.all().order_by('-thoigianvao')
        
        # Apply date filters if provided
        if from_date:
            try:
                from_date = datetime.strptime(from_date, '%Y-%m-%d').date()
                parking_records = parking_records.filter(thoigianvao__date__gte=from_date)
            except ValueError:
                pass
                
        if to_date:
            try:
                to_date = datetime.strptime(to_date, '%Y-%m-%d').date()
                parking_records = parking_records.filter(thoigianvao__date__lte=to_date)
            except ValueError:
                pass
        
        # Apply vehicle type filter if not 'all'
        if vehicle_type != 'all':
            parking_records = parking_records.filter(bienso__loaixe=vehicle_type)
        
        # Calculate statistics
        total_entries = parking_records.count()
        car_count = parking_records.filter(bienso__loaixe='car').count()
        motorcycle_count = parking_records.filter(bienso__loaixe='motorcycle').count()
        bike_count = parking_records.filter(bienso__loaixe='bike').count()
        
        # Calculate total revenue
        total_revenue = 0
        for record in parking_records:
            if record.thoigianra:  # Only calculate for completed parking sessions
                try:
                    duration = record.thoigianra - record.thoigianvao
                    hours = duration.total_seconds() / 3600
                    # Get price per hour for the vehicle type
                    price_per_hour = Giave.objects.get(loaixe=record.bienso.loaixe).giatheogio
                    total_revenue += price_per_hour * hours
                except (Giave.DoesNotExist, AttributeError):
                    continue
        
        context = {
            'parking_records': parking_records,
            'total_entries': total_entries,
            'car_count': car_count,
            'motorcycle_count': motorcycle_count,
            'bike_count': bike_count,
            'total_revenue': total_revenue,
            'from_date': from_date,
            'to_date': to_date,
            'vehicle_type': vehicle_type,
        }
        
        return render(request, 'vehicle_report.html', context)
    except Exception as e:
        # Log the error for debugging
        print(f"Error in vehicle_report view: {str(e)}")
        # Return empty context in case of error
        return render(request, 'vehicle_report.html', {
            'parking_records': [],
            'total_entries': 0,
            'car_count': 0,
            'motorcycle_count': 0,
            'bike_count': 0,
            'total_revenue': 0,
            'from_date': from_date,
            'to_date': to_date,
            'vehicle_type': vehicle_type,
        })

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



# ===================================QLX=======================================
# View để xem danh sách xe
import math
from django.utils import timezone
from django.shortcuts import render
from .models import Xe, Luotravao

def vehicle_management(request):
    vehicles = Xe.objects.all()
    data = []

    for vehicle in vehicles:
        # Lấy tất cả các lượt đã có thời gian ra
        luots = Luotravao.objects.filter(bienso=vehicle).exclude(thoigianra=None)

        # Tính tổng tiền
        tong_tien = 0
        for luot in luots:
            thoigianvao = luot.thoigianvao
            thoigianra = luot.thoigianra
            duration = (thoigianra - thoigianvao).total_seconds() / 3600  # số giờ
            duration = math.ceil(duration)  # làm tròn lên

            if vehicle.loaixe == 'Oto':
                tong_tien += duration * 30000  # 30k/giờ
            elif vehicle.loaixe == 'Xe máy':
                tong_tien += duration * 10000  # 10k/giờ

        # Lấy vị trí hiện tại nếu có
        latest_luot = Luotravao.objects.filter(bienso=vehicle, trangthai='Đang gửi').order_by('-thoigianvao').first()
        if latest_luot and latest_luot.mavitri:
            ten_vitri = latest_luot.mavitri.tenvitri
        else:
            ten_vitri = 'Chưa có vị trí'

        data.append({
            'vehicle': vehicle,
            'ten_vitri': ten_vitri,
            'tong_tien': tong_tien,
        })

    return render(request, 'vehicle_management.html', {'vehicles': data})




def vehicle_edit(request, pk):
    vehicle = get_object_or_404(Xe, pk=pk)
    if request.method == 'POST':
        # Cập nhật từng trường dữ liệu từ request.POST
        vehicle.bienso = request.POST.get('bienso')
        vehicle.loaixe = request.POST.get('loaixe')
        # Nếu có thêm trường makh thì thêm:
        makh = request.POST.get('makh')
        if makh:
            vehicle.makh_id = makh  # chú ý, nếu bạn dùng khóa ngoại thì cần gán _id

        vehicle.save()
        return redirect('vehicle_management')
    return render(request, 'vehicle_edit.html', {'vehicle': vehicle})


# View để xóa xe
def vehicle_delete(request, pk):
    vehicle = get_object_or_404(Xe, pk=pk)
    if request.method == 'POST':
        vehicle.delete()
        return redirect('vehicle_management')
    return render(request, 'vehicle_confirm_delete.html', {'vehicle': vehicle})

def parking_status(request):
    # Lấy danh sách xe đang đỗ (chưa có lượt ra)
    vehicles = Luotravao.objects.filter(thoigianra__isnull=True)

    # Lấy tất cả vị trí đỗ xe
    parking_spots = Vitridoxe.objects.all()

    # Tạo từ điển các vị trí đã bị chiếm
    occupied_slots = {}
    for vehicle in vehicles:
        if vehicle.mavitri:
            spot_name = vehicle.mavitri.tenvitri
            occupied_slots[spot_name] = vehicle.bienso

    # Chia vị trí đỗ xe thành 4 tầng theo chữ cái đầu
    floor1_spots = [spot for spot in parking_spots if 'A' <= spot.tenvitri[0] <= 'G']
    floor2_spots = [spot for spot in parking_spots if 'H' <= spot.tenvitri[0] <= 'N']
    floor3_spots = [spot for spot in parking_spots if 'O' <= spot.tenvitri[0] <= 'U']
    floor4_spots = [spot for spot in parking_spots if 'V' <= spot.tenvitri[0] <= 'Z']

    context = {
        'floor1_spots': floor1_spots,
        'floor2_spots': floor2_spots,
        'floor3_spots': floor3_spots,
        'floor4_spots': floor4_spots,
        'occupied_slots': occupied_slots,  # Gửi danh sách các slot đã chiếm
    }

    return render(request, 'parking_status.html', context)

def xe_vao_bai(bienso, loaixe):
    # Tìm 1 vị trí còn trống
    vitri = Vitridoxe.objects.filter(is_occupied=False).first()
    if not vitri:
        return "Bãi đã đầy"  # Không tìm thấy vị trí trống nào

    # Nếu còn trống -> tạo đối tượng Xe
    xe = Xe.objects.create(
        bienso=bienso,
        loaixe=loaixe,
        vitridoxe=vitri
    )

    # Cập nhật vị trí đó thành đã có xe
    vitri.is_occupied = True
    vitri.save()

    return f"Xe {bienso} vào chỗ {vitri.tenvitri}"
def xe_ra_bai(request, xe_id):
    try:
        xe = Xe.objects.get(id=xe_id)
        luot = Luotravao.objects.filter(xe=xe, thoigianra__isnull=True).last()
        
        if luot:
            luot.thoigianra = timezone.now()
            luot.save()

        # Trả lại vị trí
        if xe.vitridoxe:
            vitri = xe.vitridoxe
            vitri.is_occupied = False
            vitri.save()

        xe.vitridoxe = None
        xe.save()

        messages.success(request, f"Xe {xe.bienso} đã ra khỏi bãi.")
    except Xe.DoesNotExist:
        messages.error(request, "Xe không tồn tại.")

    return redirect('vehicle_management')


def export_vehicle_report(request):
    try:
        # Get filter parameters from request
        from_date = request.GET.get('from_date')
        to_date = request.GET.get('to_date')
        vehicle_type = request.GET.get('vehicle_type', 'all')
        
        # Base query
        parking_records = Luotravao.objects.all()
        all_records = Luotravao.objects.all()
        
        # Apply filters
        if from_date:
            parking_records = parking_records.filter(thoigianvao__date__gte=from_date)
        if to_date:
            parking_records = parking_records.filter(thoigianvao__date__lte=to_date)
        if vehicle_type != 'all':
            parking_records = parking_records.filter(bienso__loaixe=vehicle_type)
        
        # Create Excel workbook and worksheet
        response = HttpResponse(content_type='application/ms-excel')
        response['Content-Disposition'] = f'attachment; filename="vehicle_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.xls"'
        
        wb = xlwt.Workbook(encoding='utf-8')
        ws = wb.add_sheet('Báo cáo xe')
        
        # Add headers
        headers = ['STT', 'Ngày', 'Biển số xe', 'Loại xe', 'Giờ vào', 'Giờ ra', 'Thời gian giữ', 'Phí (VNĐ)']
        for col, header in enumerate(headers):
            ws.write(0, col, header)

        # Add data
        for row, record in enumerate(parking_records, start=1):
            try:
                ws.write(row, 0, row)  # STT
                ws.write(row, 1, record.thoigianvao.strftime('%d/%m/%Y'))  # Ngày
                ws.write(row, 2, record.bienso.bienso)  # Biển số xe
                ws.write(row, 3, record.bienso.loaixe)  # Loại xe
                ws.write(row, 4, record.thoigianvao.strftime('%H:%M'))  # Giờ vào
                ws.write(row, 5, record.thoigianra.strftime('%H:%M') if record.thoigianra else 'Chưa ra')  # Giờ ra
                
                # Calculate duration
                if record.thoigianra:
                    duration = record.thoigianra - record.thoigianvao
                    hours = duration.total_seconds() / 3600
                    ws.write(row, 6, f"{int(hours)} giờ {int((hours % 1) * 60)} phút")
                else:
                    ws.write(row, 6, 'Đang đỗ')
                
                # Calculate fee
                if record.thoigianra:
                    try:
                        price_per_hour = Giave.objects.get(loaixe=record.bienso.loaixe).giatheogio
                        fee = price_per_hour * hours
                        ws.write(row, 7, f"{fee:,.0f}")
                    except (Giave.DoesNotExist, AttributeError):
                        ws.write(row, 7, '-')
                else:
                    ws.write(row, 7, '-')
            except Exception as e:
                print(f"Error processing record {record.id}: {str(e)}")
                continue
        
            wb.save(response)
            return response

        # Add summary
        summary_row = len(parking_records) + 2
        ws.write(summary_row, 0, 'Thống kê')
        ws.write(summary_row + 1, 0, 'Tổng số lượt xe:')
        ws.write(summary_row + 1, 1, parking_records.count())
        ws.write(summary_row + 2, 0, 'Ô tô:')
        ws.write(summary_row + 2, 1, parking_records.filter(bienso__loaixe='Ô tô').count())
        ws.write(summary_row + 3, 0, 'Xe máy:')
        ws.write(summary_row + 3, 1, parking_records.filter(bienso__loaixe='Xe máy').count())
        ws.write(summary_row + 4, 0, 'Xe đạp:')
        ws.write(summary_row + 4, 1, parking_records.filter(bienso__loaixe='Xe đạp').count())
                
        # Calculate total revenue
        total_revenue = 0
        for record in parking_records:
            if record.thoigianra:
                try:
                    duration = record.thoigianra - record.thoigianvao
                    hours = duration.total_seconds() / 3600
                    price_per_hour = Giave.objects.get(loaixe=record.bienso.loaixe).giatheogio
                    total_revenue += price_per_hour * hours
                except (Giave.DoesNotExist, AttributeError):
                    continue
        
        ws.write(summary_row + 5, 0, 'Tổng doanh thu:')
        ws.write(summary_row + 5, 1, f"{total_revenue:,.0f} VNĐ")
        
        wb.save(response)
        return response
    except Exception as e:
        print(f"Error in export_vehicle_report: {str(e)}")
        return HttpResponse("Có lỗi xảy ra khi xuất báo cáo. Vui lòng thử lại sau.")