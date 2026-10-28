from datetime import date, time
from io import BytesIO
import pandas as pd
import pytest

from src.config import BuildOptions
from src.parser import extract_year, extract_dept_from_regno, safe_sheet_name, find_column
from src.grouping import get_group_cols, build_summary
from src.excel_io import process_excel

OPTIONS = BuildOptions(
    group_mode="Year + Department",
    dept_source="From RegNo",
    add_summary=True,
    sort_by_regno=True,
    base_century=2000,
)

def workbook(rows, columns=("regno", "name")):
    df = pd.DataFrame(rows, columns=list(columns))
    stream = BytesIO()
    df.to_excel(stream, index=False)
    stream.seek(0)
    return stream

def test_extract_year_and_department():
    assert extract_year("24CSE001") == 2024
    assert extract_year("2024CSE001") == 2024
    assert extract_year("not-a-regno") is None
    assert extract_dept_from_regno("24cse001") == "CSE"
    assert extract_dept_from_regno("unknown") == "UNKNOWN"

def test_safe_sheet_name_is_excel_compatible():
    assert safe_sheet_name("CSE/AI:2026") == "CSE_AI_2026"
    assert len(safe_sheet_name("x" * 50)) == 31

def test_find_column_ignores_spaces_and_case():
    df = pd.DataFrame(columns=["Register Number", "Student Name"])
    assert find_column(df, ["regno", "register number"]) == "Register Number"

def test_grouping_summary_counts_rows():
    df = pd.DataFrame({"Year": [2024, 2024, 2025], "Department": ["CSE", "CSE", "ECE"]})
    summary = build_summary(df, get_group_cols("Year + Department"))
    assert summary["count"].sum() == 3
    assert len(summary) == 2

def test_process_excel_creates_downloadable_workbook():
    uploaded = workbook([("24CSE001", "Asha"), ("24ECE002", "Bala")])
    df, summary, filename, output = process_excel(
        uploaded, OPTIONS, "Demo Event", date(2026, 10, 28), time(9, 0), time(10, 0)
    )
    assert len(df) == 2
    assert summary["count"].sum() == 2
    assert filename.endswith(".xlsx")
    assert output[:2] == b"PK"
    result = pd.ExcelFile(BytesIO(output))
    assert "Summary" in result.sheet_names

def test_process_excel_rejects_missing_required_columns():
    uploaded = workbook([("24CSE001", "Asha")], columns=("regno", "email"))
    with pytest.raises(ValueError, match="Column not found: Name"):
        process_excel(uploaded, OPTIONS, "Demo", date.today(), time(9), time(10))

def test_process_excel_rejects_duplicate_registration_numbers():
    uploaded = workbook([("24CSE001", "Asha"), ("24CSE001", "Bala")])
    with pytest.raises(ValueError, match="Duplicate registration number"):
        process_excel(uploaded, OPTIONS, "Demo", date.today(), time(9), time(10))

def test_process_excel_rejects_blank_student_name():
    uploaded = workbook([("24CSE001", "")])
    with pytest.raises(ValueError, match="blank student name"):
        process_excel(uploaded, OPTIONS, "Demo", date.today(), time(9), time(10))
