# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cambien(models.Model):
    cambienid = models.CharField(db_column='CamBienID', primary_key=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    loai = models.CharField(db_column='Loai', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    vitri = models.CharField(db_column='ViTri', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    trangthai = models.CharField(db_column='TrangThai', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'CamBien'


class Camera(models.Model):
    cameraid = models.CharField(db_column='CameraID', primary_key=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    chucnang = models.CharField(db_column='ChucNang', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    vitrilapdat = models.CharField(db_column='ViTriLapDat', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    trangthai = models.CharField(db_column='TrangThai', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Camera'


class Chitiethoadon(models.Model):
    chitiethoadonid = models.CharField(db_column='ChiTietHoaDonID', primary_key=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    hoadonid = models.ForeignKey('Hoadon', models.DO_NOTHING, db_column='HoaDonID', blank=True, null=True)  # Field name made lowercase.
    lanravao = models.ForeignKey('Lanvaora', models.DO_NOTHING, db_column='LanRaVao', blank=True, null=True)  # Field name made lowercase.
    ngaylap = models.DateTimeField(db_column='NgayLap', blank=True, null=True)  # Field name made lowercase.
    phuongthucthanhtoan = models.CharField(db_column='PhuongThucThanhToan', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sotien = models.FloatField(db_column='SoTien', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ChiTietHoaDon'


class Hoadon(models.Model):
    hoadonid = models.CharField(db_column='HoaDonID', primary_key=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    phuongthucthanhtoan = models.CharField(db_column='PhuongThucThanhToan', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    tudongtinhtien = models.BooleanField(db_column='TuDongTinhTien', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'HoaDon'


class Khachhang(models.Model):
    khachhangid = models.CharField(db_column='KhachHangID', primary_key=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tenkhachhang = models.CharField(db_column='TenKhachHang', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sodienthoai = models.CharField(db_column='SoDienThoai', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='Email', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'KhachHang'


class Lanvaora(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    maqr = models.CharField(db_column='MaQR', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    nhanvienid = models.ForeignKey('Nhanvien', models.DO_NOTHING, db_column='NhanVienID', blank=True, null=True)  # Field name made lowercase.
    xe = models.ForeignKey('Xe', models.DO_NOTHING, db_column='Xe', blank=True, null=True)  # Field name made lowercase.
    vitridoxe = models.ForeignKey('Vitridoxe', models.DO_NOTHING, db_column='ViTriDoXe', blank=True, null=True)  # Field name made lowercase.
    theguixe = models.ForeignKey('Theguixe', models.DO_NOTHING, db_column='TheGuiXe', blank=True, null=True)  # Field name made lowercase.
    thoigianvao = models.DateTimeField(db_column='ThoiGianVao', blank=True, null=True)  # Field name made lowercase.
    thoigianra = models.DateTimeField(db_column='ThoiGianRa', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'LanVaoRa'


class Nhanvien(models.Model):
    nhanvienid = models.CharField(db_column='NhanVienID', primary_key=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    hoten = models.CharField(db_column='HoTen', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    diachi = models.CharField(db_column='DiaChi', max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    sodienthoai = models.CharField(db_column='SoDienThoai', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ngaysinh = models.DateTimeField(db_column='NgaySinh', blank=True, null=True)  # Field name made lowercase.
    chucvu = models.CharField(db_column='ChucVu', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'NhanVien'


class Taikhoan(models.Model):
    tendangnhap = models.CharField(db_column='TenDangNhap', primary_key=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    matkhau = models.CharField(db_column='MatKhau', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    nhanvienid = models.ForeignKey(Nhanvien, models.DO_NOTHING, db_column='NhanVienID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TaiKhoan'


class Theguixe(models.Model):
    theguixeid = models.CharField(db_column='TheGuiXeID', primary_key=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    loaithe = models.CharField(db_column='LoaiThe', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    ngaycap = models.DateTimeField(db_column='NgayCap', blank=True, null=True)  # Field name made lowercase.
    ngayhethan = models.DateTimeField(db_column='NgayHetHan', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TheGuiXe'


class Vitridoxe(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    tenvitri = models.CharField(db_column='TenViTri', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    khuvuc = models.CharField(db_column='KhuVuc', max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    trangthai = models.CharField(db_column='TrangThai', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'ViTriDoXe'


class Xe(models.Model):
    xeid = models.CharField(db_column='XeID', primary_key=True, max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS')  # Field name made lowercase.
    bienso = models.CharField(db_column='BienSo', max_length=20, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    loaixe = models.CharField(db_column='LoaiXe', max_length=50, db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)  # Field name made lowercase.
    chuxe = models.ForeignKey(Khachhang, models.DO_NOTHING, db_column='ChuXe', blank=True, null=True)  # Field name made lowercase.
    anhxe = models.BinaryField(db_column='AnhXe', blank=True, null=True)  # Field name made lowercase.
    imgurl = models.BinaryField(db_column='Imgurl', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'Xe'


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    first_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    last_name = models.CharField(max_length=150, db_collation='SQL_Latin1_General_CP1_CI_AS')
    email = models.CharField(max_length=254, db_collation='SQL_Latin1_General_CP1_CI_AS')
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS', blank=True, null=True)
    object_repr = models.CharField(max_length=200, db_collation='SQL_Latin1_General_CP1_CI_AS')
    action_flag = models.SmallIntegerField()
    change_message = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')
    model = models.CharField(max_length=100, db_collation='SQL_Latin1_General_CP1_CI_AS')

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    name = models.CharField(max_length=255, db_collation='SQL_Latin1_General_CP1_CI_AS')
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40, db_collation='SQL_Latin1_General_CP1_CI_AS')
    session_data = models.TextField(db_collation='SQL_Latin1_General_CP1_CI_AS')
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class Sysdiagrams(models.Model):
    name = models.CharField(max_length=128, db_collation='SQL_Latin1_General_CP1_CI_AS')
    principal_id = models.IntegerField()
    diagram_id = models.AutoField(primary_key=True)
    version = models.IntegerField(blank=True, null=True)
    definition = models.BinaryField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'sysdiagrams'
        unique_together = (('principal_id', 'name'),)
