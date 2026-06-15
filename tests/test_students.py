from src.db import get_all_students

def test_students_exist():
    students = get_all_students()
    assert len(students) >= 5