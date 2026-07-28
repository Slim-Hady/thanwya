#!/usr/bin/env python3
"""Convert the results Excel file to chunked JSON for the website."""

import json
import os
import openpyxl

EXCEL_FILE = "نتيجة ثانوية عامة نظام حديث(1).xlsx"
OUTPUT_DIR = "chunks"
CHUNK_SIZE = 50000

os.makedirs(OUTPUT_DIR, exist_ok=True)

wb = openpyxl.load_workbook(EXCEL_FILE, read_only=True)
ws = wb.active

students = []
for row in ws.iter_rows(min_row=2, values_only=True):
    seating_no, arabic_name, total_degree, student_case_desc = row
    if seating_no is None:
        continue
    students.append([
        int(seating_no),
        str(arabic_name).strip() if arabic_name else "",
        float(total_degree) if total_degree else 0,
        str(student_case_desc).strip() if student_case_desc else "",
    ])

wb.close()

manifest = []
for i in range(0, len(students), CHUNK_SIZE):
    chunk = students[i:i + CHUNK_SIZE]
    chunk_file = os.path.join(OUTPUT_DIR, f"{i // CHUNK_SIZE}.json")
    with open(chunk_file, "w", encoding="utf-8") as f:
        json.dump(chunk, f, ensure_ascii=True, separators=(",", ":"))
    manifest.append({
        "file": f"{i // CHUNK_SIZE}.json",
        "min_id": chunk[0][0],
        "max_id": chunk[-1][0],
        "count": len(chunk),
    })

with open(os.path.join(OUTPUT_DIR, "manifest.json"), "w", encoding="utf-8") as f:
    json.dump(manifest, f)

print(f"Wrote {len(students)} students in {len(manifest)} chunks to {OUTPUT_DIR}/")
