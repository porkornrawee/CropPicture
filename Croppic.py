import os
import datetime
from pathlib import Path
from rembg import remove
from PIL import Image

# พยายาม Import ตัวอ่านไฟล์ HEIC (สำหรับ Mac/iPhone)
try:
    from pillow_heif import register_heif_opener
    register_heif_opener()
except ImportError:
    print("⚠️ ไม่พบ pillow-heif: หากมีไฟล์ .HEIC โปรแกรมอาจเปิดไม่ได้ (แก้โดย pip install pillow-heif)")

def process_images():
    # 1. ตั้งค่าโฟลเดอร์
    input_folder = "inputs"
    
    # สร้างชื่อโฟลเดอร์ปลายทางตาม วัน_เวลา
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_folder = f"rmbg_{timestamp}"

    # ตรวจสอบว่ามีโฟลเดอร์ inputs ไหม
    if not os.path.exists(input_folder):
        os.makedirs(input_folder)
        print(f"❌ ไม่พบโฟลเดอร์ '{input_folder}'")
        print(f"✅ ผมสร้างโฟลเดอร์ '{input_folder}' ให้แล้ว เอารูปไปใส่แล้วรันใหม่นะครับ")
        return

    # สร้างโฟลเดอร์ผลลัพธ์
    os.makedirs(output_folder, exist_ok=True)

    # นามสกุลไฟล์ที่รองรับ
    valid_extensions = {'.jpg', '.jpeg', '.png', '.heic', '.webp', '.bmp'}
    
    files = os.listdir(input_folder)
    count = 0
    
    print(f"🚀 กำลังเริ่มงาน... ผลลัพธ์จะอยู่ที่โฟลเดอร์: {output_folder}")

    for filename in files:
        file_path = Path(input_folder) / filename
        
        # เช็คว่าเป็นไฟล์ภาพหรือไม่
        if file_path.suffix.lower() not in valid_extensions:
            continue

        try:
            print(f"⏳ กำลังตัดพื้นหลัง: {filename} ...", end="\r")
            
            # เปิดรูปภาพ
            with Image.open(file_path) as img:
                # ตัดพื้นหลัง
                output = remove(img)
                
                # ตั้งชื่อไฟล์ใหม่ (บังคับเซฟเป็น .png เพื่อให้โปร่งใส)
                new_filename = f"{file_path.stem}.png"
                output_path = Path(output_folder) / new_filename
                
                # บันทึก
                output.save(output_path)
                count += 1
                
        except Exception as e:
            print(f"\n❌ เกิดข้อผิดพลาดกับไฟล์ {filename}: {e}")

    print(f"\n\n✅ เสร็จเรียบร้อย! จัดการไปทั้งหมด {count} รูป")
    print(f"📂 ไปดูรูปได้ที่โฟลเดอร์: {output_folder}")

if __name__ == "__main__":
    
    process_images()