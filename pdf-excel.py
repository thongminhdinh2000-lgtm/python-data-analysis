import os
import pdfplumber
import pandas as pd

# ==========================
# Đường dẫn
# ==========================
INPUT_FOLDER = r"D:\DATASQL\Python\Input"
OUTPUT_FOLDER = r"D:\DATASQL\Python\Output"

# Nếu chưa có thư mục Output thì tạo
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==========================
# Hàm chuyển PDF sang Excel
# ==========================
def pdf_to_excel(pdf_path, excel_path):

    all_tables = []

    with pdfplumber.open(pdf_path) as pdf:
        for page in pdf.pages:

            tables = page.extract_tables()

            if tables:
                for table in tables:
                    if len(table) > 1:
                        df = pd.DataFrame(table[1:], columns=table[0])
                        all_tables.append(df)

    if all_tables:
        result = pd.concat(all_tables, ignore_index=True)
        result.to_excel(excel_path, index=False)
        return True
    else:
        return False


# ==========================
# Chạy tất cả file PDF
# ==========================

files = [f for f in os.listdir(INPUT_FOLDER) if f.lower().endswith(".pdf")]

print(f"Tìm thấy {len(files)} file PDF\n")

for file in files:

    pdf_file = os.path.join(INPUT_FOLDER, file)

    excel_name = os.path.splitext(file)[0] + ".xlsx"

    excel_file = os.path.join(OUTPUT_FOLDER, excel_name)

    try:
        ok = pdf_to_excel(pdf_file, excel_file)

        if ok:
            print(f"✔ Đã chuyển: {file}")
        else:
            print(f"⚠ Không tìm thấy bảng trong: {file}")

    except Exception as e:
        print(f"❌ Lỗi {file}")
        print(e)

print("\nHoàn thành!")
