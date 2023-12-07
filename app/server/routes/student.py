from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from db.database import (
    add_student,
    delete_student,
    retrieve_student,
    retrieve_students,
    update_student,
)

from db.models.student import (
    ErrorResponseModel,
    ResponseModel,
    StudentSchema,
    UpdateStudentModel,
)

router = APIRouter()

@router.post("/", response_description="Student data added into the database")
async def add_student_data(student: StudentSchema = Body(...)):
    student = jsonable_encoder(student)
    new_student = await add_student(student)
    if len(new_student):
        response = ResponseModel(new_student, "Student added successfully.")
    else:
        response = ErrorResponseModel("database not connected", 500, "student could not be added" )
    return response

@router.get("/", response_description="Students retrieved")
async def read_all_students():
    students =  await retrieve_students()
    if len(students):
        response = ResponseModel(students, "Students informations successfully recovered.")
    else:
        response = ResponseModel(students, "Empty list returned")
    return response

@router.get("/{id}")
async def read_one_student(id : str):
    student = await retrieve_student(id)
    if len(student):
        response = ResponseModel(student, "Student information successfully recovered." )
    else:
        response = ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")
    return response

@router.delete("/{id}", response_description="Student data deleted from the database")
async def delete_student_data(id : str):
    del_student = await delete_student(id)
    if len(del_student):
        response = ResponseModel(del_student, "Student delete successfully.")
    else:
        response = ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")
    return response

@router.put("/{id}")
async def uptade_one_student(id : str, data : UpdateStudentModel):
    req = {k : v for k, v in data.dict().items() if v is not None}
    student = await update_student(id, req)
    if len(student):
        response = ResponseModel(student, "Student update successfully.")
    else:
        response = ErrorResponseModel("An error occurred.", 404, "Student doesn't exist.")
    return response


