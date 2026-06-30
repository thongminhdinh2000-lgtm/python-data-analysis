import os
import shutil
from datetime import datetime

import pandas as pd

# ==========================
# Khai báo đường dẫn
# ==========================

INPUT_FOLDER = r"D:\DataSQL\Input"
OUTPUT_FOLDER = r"D:\DataSQL\Output"
ARCHIVE_FOLDER = r"D:\DataSQL\Archive"

# Sheet cần đọc
SHEET_NAME = 0      # Sheet đầu tiên

# ==========================
# Tạo thư mục nếu chưa có
# ==========================

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

# ==========================
# Lấy danh sách file
# ==========================

excel_files = [
    f for f in os.listdir(INPUT_FOLDER)
    if f.endswith(".xlsx") or f.endswith(".xls")
]

if len(excel_files) == 0:
    print("Không có file Excel.")
    exit()

# ==========================
# Đọc và gộp
# ==========================

dataframes = []

for file in excel_files:

    file_path = os.path.join(INPUT_FOLDER, file)

    try:

        df = pd.read_excel(
            file_path,
            sheet_name=SHEET_NAME
        )

        # thêm tên file nguồn
        df["SourceFile"] = file

        dataframes.append(df)

        print(f"Đọc thành công: {file}")

    except Exception as e:

        print(f"Lỗi {file}: {e}")

# concat sẽ tự thêm cột mới nếu khác nhau
merged_df = pd.concat(
    dataframes,
    ignore_index=True,
    sort=False
)

# ==========================
# Xuất file
# ==========================

output_file = os.path.join(
    OUTPUT_FOLDER,
    f"TongHop_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
)

merged_df.to_excel(
    output_file,
    index=False
)

print("Đã xuất:", output_file)

# ==========================
# Chuyển file sang Archive
# ==========================

for file in excel_files:

    src = os.path.join(INPUT_FOLDER, file)
    dst = os.path.join(ARCHIVE_FOLDER, file)

    # Nếu Archive đã có file cùng tên thì thêm thời gian
    if os.path.exists(dst):

        name, ext = os.path.splitext(file)

        dst = os.path.join(
            ARCHIVE_FOLDER,
            f"{name}_{datetime.now():%Y%m%d_%H%M%S}{ext}"
        )

    shutil.move(src, dst)

print("Đã chuyển toàn bộ file sang Archive.")
print("Hoàn thành!")