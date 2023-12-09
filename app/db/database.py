import motor.motor_asyncio
from bson.objectid import ObjectId
from .config import MONGO_CREDENTIALS, MONGO_DB_NAME

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_CREDENTIALS)
db = client.students
student_collection = db.get_collection(MONGO_DB_NAME)


def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "email": student["email"],
        "course_of_study": student["course_of_study"],
        "year": student["year"],
        "GPA": student["gpa"],
    }

async def retrieve_students() -> list[dict]:
    students = []
    async for student in student_collection.find():
        students.append(student_helper(student))
    return students

async def add_student(student_data: dict) -> dict:
    student = await student_collection.insert_one(student_data)
    new_student = await student_collection.find_one({'_id' : student.inserted_id})
    ans = {}
    if new_student:
        ans = student_helper(new_student)
    return ans

async def retrieve_student(id : str) -> dict:
    student = await student_collection.find_one({"_id" : ObjectId(id)})
    ans = dict()
    if student:
        ans = student_helper(student)
    return ans

async def update_student(id : str, data : dict) -> dict:
    student = await student_collection.find_one({"_id" : ObjectId(id)})
    ans = {}
    if student:
        update_student = await student_collection.update_one(
            {"_id" : ObjectId(id)}, {'$set' : data}
        )
        if update_student:
            student = await student_collection.find_one({'_id' : ObjectId(id)})
            ans = student_helper(student)
    return ans

async def delete_student(id : str) -> dict:
    student = await student_collection.find_one({'_id' : ObjectId(id)})
    ans = {}
    if student:
        del_student = await student_collection.delete_one({'_id' : ObjectId(id)})
        if del_student:
            ans = student_helper(student)
    return ans