import cv2
import easyocr
import uuid
import os
import django
from datetime import datetime
from PIL import Image
import io

# Cấu hình Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'parking_system.settings')  # Đổi thành tên project của bạn
django.setup()

from system.models import Xe, Luotravao, Vitridoxe  # Đổi lại đúng app và model của bạn

reader = easyocr.Reader(['vi', 'en'])

def phan_loai_theo_dong(bien_so_dong_tren):
    text = bien_so_dong_tren.replace(" ", "").replace("-", "").upper()
    if len(text) == 3:
        return 'Xe 4 bánh'
    elif len(text) == 4:
        return 'Xe 2 bánh'
    return 'Không xác định'

# Thư mục lưu ảnh biển số
img_save_path = 'media/parking_images/'

# Tạo thư mục nếu chưa có
if not os.path.exists(img_save_path):
    os.makedirs(img_save_path)

cap = cv2.VideoCapture(0)
print("Nhấn 'c' để chụp ảnh và nhận diện biển số, hoặc 'q' để thoát.")

# Biến lưu biển số và loại xe để sau này lưu vào SQL khi thoát chương trình
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

        results_sorted = sorted(results, key=lambda r: r[0][0][1])
        texts = [t[1] for t in results_sorted if t[2] > 0.5]

        if len(texts) < 2:
            print("Không đủ 2 dòng để xác định biển số.")
            continue

        dong_tren = texts[0].replace(" ", "").replace("-", "").upper()
        dong_duoi = texts[1].replace(" ", "").replace("-", "").upper()
        bien_so_ket_hop = dong_tren + dong_duoi

        if 7 <= len(bien_so_ket_hop) <= 10:
            # Lưu biển số và loại xe vào biến tạm khi nhận diện thành công
            bien_so_quet = bien_so_ket_hop
            loai_xe_quet = phan_loai_theo_dong(dong_tren)
            thoigian_quet = datetime.now()

            # Lưu ảnh biển số vào thư mục
            img_filename = f"{bien_so_quet}_{uuid.uuid4().hex}.jpg"
            img_full_path = os.path.join(img_save_path, img_filename)

            # Lưu ảnh vào file
            cv2.imwrite(img_full_path, frame)

            img_path_quet = img_full_path
            print(f"🔍 Biển số nhận diện: {bien_so_quet} | Loại xe: {loai_xe_quet} | Thời gian nhận diện: {thoigian_quet}")
        else:
            print(f"⛔ Biển số không hợp lệ: {bien_so_ket_hop}")

    elif key == ord('q') or (key == ord('c') and bien_so_quet and loai_xe_quet and thoigian_quet and img_path_quet):
    # Sau khi nhấn 'q' hoặc sau khi nhận diện biển số thành công, lưu dữ liệu vào SQL
        if bien_so_quet and loai_xe_quet and thoigian_quet and img_path_quet:
            xe = Xe.objects.filter(bienso=bien_so_quet).first()
            
            if xe:
                # Xe đã vào, giờ là xe ra
                luot = Luotravao.objects.filter(bienso=xe, thoigianra__isnull=True).first()
                
                if luot:
                    luot.thoigianra = datetime.now()
                    luot.save()
                    print(f"🚗 Xe ra: {bien_so_quet} | Thời gian ra: {luot.thoigianra}")
                else:
                    print(f"⚠️ Không tìm thấy lượt vào cho xe biển số: {bien_so_quet}")
            else:
                # Xe mới vào
                xe = Xe(
                    bienso=bien_so_quet,
                    loaixe=loai_xe_quet,
                    makh=None,
                )
                xe.save()

                luot = Luotravao(
                    bienso=xe,
                    thoigianvao=thoigian_quet,
                    anhvao=img_path_quet,
                )
                luot.save()
                print(f"✅ Xe vào: {bien_so_quet} | Thời gian vào: {thoigian_quet} | Đường dẫn ảnh: {img_path_quet}")
        else:
            print("⚠️ Không có dữ liệu biển số để lưu.")

        break  # THÊM LỆNH break() để thoát vòng lặp


cap.release()
cv2.destroyAllWindows()
