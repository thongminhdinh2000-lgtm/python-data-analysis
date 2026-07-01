import os
import pandas as pd
import tabula

# ==========================
# Đường dẫn
# ==========================
INPUT_FOLDER = r"D:\DATASQL\Input"
OUTPUT_FOLDER = r"D:\DATASQL\Output"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# ==========================
# Lấy danh sách PDF
# ==========================
pdf_files = [f for f in os.listdir(INPUT_FOLDER)
             if f.lower().endswith(".pdf")]

print(f"Tìm thấy {len(pdf_files)} file PDF\n")

# ==========================
# Chuyển từng file
# ==========================
for pdf in pdf_files:

    pdf_path = os.path.join(INPUT_FOLDER, pdf)

    excel_path = os.path.join(
        OUTPUT_FOLDER,
        os.path.splitext(pdf)[0] + ".xlsx"
    )

    try:

        tables = tabula.read_pdf(
            pdf_path,
            pages="all",
            multiple_tables=True,
            lattice=True
        )

        if len(tables) == 0:

            tables = tabula.read_pdf(
                pdf_path,
                pages="all",
                multiple_tables=True,
                stream=True
            )

        if len(tables) == 0:
            print(f"❌ Không đọc được bảng: {pdf}")
            continue

        with pd.ExcelWriter(excel_path,
                            engine="openpyxl") as writer:

            for i, table in enumerate(tables):

                table.to_excel(
                    writer,
                    sheet_name=f"Bang_{i+1}",
                    index=False
                )

        print(f"✔ {pdf}")

    except Exception as e:

        print(f"❌ Lỗi {pdf}")
        print(e)

print("\nHoàn thành.")
