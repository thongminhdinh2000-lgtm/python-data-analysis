import os
import shutil
from datetime import datetime
import pandas as pd

# ==========================
# Khai báo thư mục
# ==========================

INPUT_FOLDER = r"D:\DataSQL\Input"
OUTPUT_FOLDER = r"D:\DataSQL\Output"
ARCHIVE_FOLDER = r"D:\DataSQL\Archive"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)
os.makedirs(ARCHIVE_FOLDER, exist_ok=True)

excel_files = [
    f for f in os.listdir(INPUT_FOLDER)
    if f.lower().endswith((".xlsx", ".xls"))
]

all_data = []

for file in excel_files:

    file_path = os.path.join(INPUT_FOLDER, file)

    try:

        # Đọc toàn bộ sheet
        raw = pd.read_excel(file_path, header=None)

        # =============================
        # Tìm dòng chứa STT
        # =============================
        header_row = None

        for i in range(len(raw)):

            row = raw.iloc[i].astype(str)

            if row.str.contains("STT", case=False).any():

                header_row = i
                break

        if header_row is None:
            print(f"Không tìm thấy bảng trong {file}")
            continue

        # =============================
        # Đọc lại từ dòng tiêu đề
        # =============================
        df = pd.read_excel(file_path, header=header_row)

        # Chuẩn hóa tên cột
        df.columns = (
            df.columns.astype(str)
            .str.replace("\n", " ", regex=False)
            .str.replace("\r", " ", regex=False)
            .str.strip()
        )

        # Đổi tên các cột nếu có xuống dòng
        rename_dict = {}

        for c in df.columns:

            if "STT" in c:
                rename_dict[c] = "STT"

            elif "Mã hàng" in c:
                rename_dict[c] = "Mã hàng"

            elif "Tên hàng" in c:
                rename_dict[c] = "Tên hàng"

            elif "Đơn vị" in c:
                rename_dict[c] = "Đơn vị"

            elif "Số lượng" in c:
                rename_dict[c] = "Số lượng"

            elif "Đơn giá" in c:
                rename_dict[c] = "Đơn giá"

        df = df.rename(columns=rename_dict)

        # Chỉ lấy các cột cần
        df = df[
            [
                "STT",
                "Mã hàng",
                "Tên hàng",
                "Đơn vị",
                "Số lượng",
                "Đơn giá"
            ]
        ]

        # Chỉ giữ các dòng STT là số
        df = df[
            pd.to_numeric(df["STT"], errors="coerce").notna()
        ]

        df = df.reset_index(drop=True)

        all_data.append(df)

        print(f"Đã đọc {file}")

    except Exception as e:

        print(file, e)

# =============================
# Gộp
# =============================

merged_df = pd.concat(
    all_data,
    ignore_index=True
)

# Xuất file

output_file = os.path.join(
    OUTPUT_FOLDER,
    f"TongHop_{datetime.now():%Y%m%d_%H%M%S}.xlsx"
)

merged_df.to_excel(
    output_file,
    index=False
)

print("Đã xuất:", output_file)

# =============================
# Chuyển file sang Archive
# =============================

for file in excel_files:

    src = os.path.join(INPUT_FOLDER, file)
    dst = os.path.join(ARCHIVE_FOLDER, file)

    if os.path.exists(dst):

        name, ext = os.path.splitext(file)

        dst = os.path.join(
            ARCHIVE_FOLDER,
            f"{name}_{datetime.now():%Y%m%d_%H%M%S}{ext}"
        )

    shutil.move(src, dst)

print("Gộp file hoàn thành.")
print(f"Tổng số file: {len(excel_files)}")
