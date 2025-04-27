import cv2
import easyocr
import uuid
import os
import django
from datetime import datetime

# Cấu hình Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking_system.settings')  # Đổi thành tên project của bạn
django.setup()

from system.models import Xe, Luotravao, Vitridoxe  # Đổi đúng app name và model

# Khởi tạo EasyOCR
reader = easyocr.Reader(['vi', 'en'])

# Thư mục lưu ảnh biển số
img_save_path = 'media/parking_images/'
if not os.path.exists(img_save_path):
    os.makedirs(img_save_path)

def phan_loai_theo_dong(bien_so_dong_tren):
    text = bien_so_dong_tren.replace(" ", "").replace("-", "").upper()
    if len(text) == 3:
        return 'Xe Ôtô'
    elif len(text) == 4:
        return 'Xe Máy'
    return 'Không xác định'

# Bắt đầu quét camera
cap = cv2.VideoCapture(0)
print("Nhấn 'c' để chụp ảnh và nhận diện biển số, hoặc 'q' để thoát.")

bien_so_quet = None
loai_xe_quet = None
thoigian_quet = None
img_path_quet = None

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

        # Sắp xếp các kết quả OCR theo tọa độ y (dòng trên trước)
        results_sorted = sorted(results, key=lambda r: r[0][0][1])
        texts = [t[1] for t in results_sorted if t[2] > 0.5]

        if len(texts) < 2:
            print("Không đủ 2 dòng để xác định biển số.")
            continue

        dong_tren = texts[0].replace(" ", "").replace("-", "").upper()
        dong_duoi = texts[1].replace(" ", "").replace("-", "").upper()
        bien_so_ket_hop = dong_tren + dong_duoi

        if 7 <= len(bien_so_ket_hop) <= 10:
            bien_so_quet = bien_so_ket_hop
            loai_xe_quet = phan_loai_theo_dong(dong_tren)
            thoigian_quet = datetime.now()

            img_filename = f"{bien_so_quet}_{uuid.uuid4().hex}.jpg"
            img_full_path = os.path.join(img_save_path, img_filename)
            cv2.imwrite(img_full_path, frame)

            img_path_quet = img_full_path
            print(f"🔍 Biển số: {bien_so_quet} | Loại xe: {loai_xe_quet} | Thời gian: {thoigian_quet}")
        else:
            print(f"⛔ Biển số không hợp lệ: {bien_so_ket_hop}")

    elif key == ord('q') or (key == ord('c') and bien_so_quet and loai_xe_quet and thoigian_quet and img_path_quet):
        if bien_so_quet and loai_xe_quet and thoigian_quet and img_path_quet:
            xe = Xe.objects.filter(bienso=bien_so_quet).first()

            if xe:
                # Xe đã tồn tại, kiểm tra lượt vào chưa ra
                luot = Luotravao.objects.filter(bienso=xe, thoigianra__isnull=True).first()

                if luot:
                    # Xe ra
                    luot.thoigianra = datetime.now()
                    luot.save()

                    if luot.mavitri:
                        Vitridoxe.objects.filter(mavitri=luot.mavitri.mavitri).update(trangthai='Trống')
                        print(f"🚗 Xe ra: {bien_so_quet} | Thời gian ra: {luot.thoigianra}")
                    else:
                        print(f"⚠️ Xe ra nhưng không có vị trí đỗ!")
                else:
                    print(f"⚠️ Không tìm thấy lượt vào cho xe biển số: {bien_so_quet}")
            else:
                # Xe mới vào
                vitri_trong = Vitridoxe.objects.filter(trangthai__iexact='Trống').first()

                if not vitri_trong:
                    vitri_trong = Vitridoxe.objects.filter(trangthai__isnull=True).first()

                if not vitri_trong:
                    print("❌ Không còn vị trí trống trong bãi xe!")
                    break


                # Tạo xe mới
                xe = Xe(
                    bienso=bien_so_quet,
                    loaixe=loai_xe_quet,
                    makh=None
                )
                xe.save()

                # Cập nhật vị trí thành đang sử dụng
                Vitridoxe.objects.filter(mavitri=vitri_trong.mavitri).update(trangthai='Đang sử dụng')

                # Tạo lượt vào
                luot = Luotravao(
                    bienso=xe,
                    thoigianvao=thoigian_quet,
                    anhvao=img_path_quet,
                    mavitri=vitri_trong,
                    trangthai='Đang gửi'
                )
                luot.save()

                print(f"✅ Xe vào: {bien_so_quet} | Vị trí: {vitri_trong.tenvitri} | Thời gian vào: {thoigian_quet} | Ảnh: {img_path_quet}")
        else:
            print("⚠️ Không có dữ liệu biển số để lưu.")

        break

cap.release()
cv2.destroyAllWindows()
