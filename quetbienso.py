import cv2
import easyocr
import uuid
import re
import django
import os
import numpy as np

# Cấu hình Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking_system.settings')  # 🔁 Đổi thành tên project của bạn
django.setup()

from system.models import Xe  # 🔁 Đổi thành tên app và model của bạn

reader = easyocr.Reader(['vi', 'en'])

def chuyen_anh_sang_binary(image):
    _, buffer = cv2.imencode('.jpg', image)
    return buffer.tobytes()

def phan_loai_theo_dong(bien_so_dong_tren):
    text = bien_so_dong_tren.replace(" ", "").replace("-", "").upper()
    if len(text) == 3:
        return 'Xe 4 bánh'
    elif len(text) == 4:
        return 'Xe 2 bánh'
    return 'Không xác định'

cap = cv2.VideoCapture(0)
print("Nhấn 'c' để chụp ảnh và nhận diện biển số, hoặc 'q' để thoát.")

bien_so_da_luu = None  # Biến ghi nhớ biển số đã lưu
xeid_da_luu = None     # Biến ghi nhớ id xe đã lưu

while True:
    ret, frame = cap.read()
    if not ret:
        print("Không đọc được camera.")
        break

    cv2.imshow("Camera", frame)
    key = cv2.waitKey(1) & 0xFF

    if key == ord('c'):
        print("🔍 Đang nhận diện biển số...")

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        results = reader.readtext(gray, detail=1)

        if not results:
            print("Không nhận diện được văn bản nào.")
            continue

        results_sorted = sorted(results, key=lambda r: r[0][0][1])
        texts = [t[1] for t in results_sorted if t[2] > 0.5]

        if len(texts) < 2:
            print("Không đủ 2 dòng để xác định biển số.")
            continue

        dong_tren = texts[0].replace(" ", "").replace("-", "").upper()
        dong_duoi = texts[1].replace(" ", "").replace("-", "").upper()
        bien_so_ket_hop = dong_tren + dong_duoi

        if 7 <= len(bien_so_ket_hop) <= 10:
            if bien_so_da_luu:
                print(f"🔁 Bạn đã lưu biển số: {bien_so_da_luu}")
                print("⚠️ Xóa biển số cũ và cập nhật lại...")

                # Xóa bản ghi cũ
                Xe.objects.filter(xeid=xeid_da_luu).delete()

            loai_xe = phan_loai_theo_dong(dong_tren)
            xeid = str(uuid.uuid4())
            anh_binary = chuyen_anh_sang_binary(frame)

            Xe.objects.create(
                xeid=xeid,
                bienso=bien_so_ket_hop,
                loaixe=loai_xe,
                chuxe=None,
                anhxe=anh_binary,
                imgurl=None
            )

            bien_so_da_luu = bien_so_ket_hop
            xeid_da_luu = xeid
            print(f"✅ Đã lưu biển số: {bien_so_ket_hop} - Loại xe: {loai_xe}")

        else:
            print(f"⛔ Biển số không hợp lệ: {bien_so_ket_hop}")

    elif key == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
