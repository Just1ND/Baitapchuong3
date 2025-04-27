import os
import shutil
import smtplib
import traceback
from datetime import datetime
from email.message import EmailMessage
from dotenv import load_dotenv
import schedule
import time

# Load biến môi trường từ .env
load_dotenv()

EMAIL_SENDER = os.getenv("EMAIL_SENDER")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
EMAIL_RECEIVER = os.getenv("EMAIL_RECEIVER")

# Thư mục chứa file database gốc và backup
DB_FILE = "D:/py_tudonghao/backup/database.sql"  # hoặc đường dẫn chính xác đến file  # hoặc "file.sql"
BACKUP_FOLDER = "backup"

# Tạo folder backup nếu chưa có
os.makedirs(BACKUP_FOLDER, exist_ok=True)

def send_email(subject, body):
    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = EMAIL_SENDER
    msg["To"] = EMAIL_RECEIVER
    msg.set_content(body)

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_SENDER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        print("Email sent!")
    except Exception as e:
        print("Failed to send email:", e)

def backup_database():
    now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_name = f"{now}_{os.path.basename(DB_FILE)}"
    backup_path = os.path.join(BACKUP_FOLDER, backup_name)

    if not os.path.exists(DB_FILE):
        print("File database.sql không tồn tại.")
        send_email("Backup Thất Bại", "Không tìm thấy file database.sql để sao lưu.")
        return
    
    try:
        shutil.copy(DB_FILE, backup_path)
        print("Backup thành công:", backup_path)
        send_email("Backup Thành Công", f"Đã sao lưu file vào:\n{backup_path}")
    except Exception as e:
        print("Backup thất bại!")
        send_email("Backup Thất Bại", f"Lỗi:\n{traceback.format_exc()}")

# Lên lịch chạy mỗi ngày lúc 00:00
schedule.every().day.at("11:51").do(backup_database)

print("Backup scheduler is running...")

# Vòng lặp chính
while True:
    schedule.run_pending()
    time.sleep(1)
