import smtplib
from email.message import EmailMessage
from pathlib import Path
import mimetypes

# ==========================
# THÔNG TIN GỬI
# ==========================

EMAIL = "thongminhdinh2000@gmail.com"
APP_PASSWORD = "wgmv xueq leak expa"

TO_EMAIL = "thongminhdinh75.dtntbt@gmail.com"

SUBJECT = "Thư cảm ơn sau buổi phỏng vấn – Thông Minh Đình"

BODY = """
Kính gửi Anh/Chị,

Em xin chân thành cảm ơn Anh/Chị đã dành thời gian trao đổi và phỏng vấn em cho vị trí Data Analyst (DA)  ngày hôm nay.

Qua buổi phỏng vấn, em càng hiểu rõ hơn về công việc, môi trường làm việc cũng như định hướng phát triển của công ty.

Điều này khiến em càng mong muốn có cơ hội được đồng hành và đóng góp vào sự phát triển của công ty.

Em xin gửi lại CV của mình trong file đính kèm để Anh/Chị tiện tham khảo.

Em rất mong nhận được phản hồi từ Anh/Chị và hy vọng sẽ có cơ hội được làm việc cùng công ty.

Kính chúc Anh/Chị sức khỏe và thành công.

Trân trọng,

Thông Minh Đình
SĐT: 0387628794
Email: thongminhdinh2000@gmail.com
"""

# ==========================
# TẠO EMAIL
# ==========================

msg = EmailMessage()

msg["From"] = EMAIL
msg["To"] = TO_EMAIL
msg["Subject"] = SUBJECT

msg.set_content(BODY)

# ==========================
# ĐÍNH KÈM CV
# ==========================

cv_path = Path(r"D:\DataSQL\gophoadon.py")      # Đường dẫn CV

mime_type, _ = mimetypes.guess_type(cv_path)

maintype, subtype = mime_type.split('/')

with open(cv_path, "rb") as f:
    msg.add_attachment(
        f.read(),
        maintype=maintype,
        subtype=subtype,
        filename=cv_path.name
    )

# ==========================
# GỬI EMAIL
# ==========================

with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
    smtp.login(EMAIL, APP_PASSWORD)
    smtp.send_message(msg)

print("Đã gửi thư cảm ơn thành công!")
