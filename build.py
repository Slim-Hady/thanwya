#!/usr/bin/env python3
"""Convert the results Excel file to a compact JSON for the website."""

import json
import openpyxl

EXCEL_FILE = "نتيجة ثانوية عامة نظام حديث(1).xlsx"
OUTPUT_FILE = "data.json"

wb = openpyxl.load_workbook(EXCEL_FILE, read_only=True)
ws = wb.active

students = []
for i, row in enumerate(ws.iter_rows(min_row=2, values_only=True)):
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

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(students, f, ensure_ascii=True, separators=(",", ":"))

print(f"Wrote {len(students)} students to {OUTPUT_FILE}")
