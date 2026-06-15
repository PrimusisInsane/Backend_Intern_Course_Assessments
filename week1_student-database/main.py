from fastapi import FastAPI
from src.db import (
    get_all_students,
    get_student,
    add_student,
    delete_student
)

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Student Management API"}


@app.get("/students")                 # Read all data on the table
def students():
    return get_all_students()



@app.get("/students/{student_id}")      # Read one item on the table
def student(student_id: int):
    return get_student(student_id)



@app.post("/students")                    # Create the data on the table
def create_student(name: str, age: int, course: str):
    return add_student({
        "name" : name,
        "age" : age,
        "course" : course
        })



@app.delete("/students/{student_id}")      # Delete the data on the table
def remove_student(student_id: int):
    return delete_student(student_id)