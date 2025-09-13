from fastapi import FastAPI, HTTPException, Query
from typing import List, Optional
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel
from datetime import datetime

# --- MongoDB setup ---
MONGO_URL = "mongodb://localhost:27017"
DB_NAME = "assessment_db"

client = AsyncIOMotorClient(MONGO_URL)
db = client[DB_NAME]
employees_collection = db["employees"]

# --- Pydantic models ---
class Employee(BaseModel):
    employee_id: str
    name: str
    department: str
    salary: float
    joining_date: datetime
    skills: List[str]

class EmployeeUpdate(BaseModel):
    name: Optional[str]
    department: Optional[str]
    salary: Optional[float]
    joining_date: Optional[datetime]
    skills: Optional[List[str]]

# --- FastAPI app ---
app = FastAPI(title="Employee API")

# Ensure unique index on employee_id
async def init_indexes():
    await employees_collection.create_index("employee_id", unique=True, name="idx_employee_id")

@app.on_event("startup")
async def startup_event():
    await init_indexes()

@app.get("/")
async def root():
    return {"message": "Employee API is running"}

# 1. Create Employee
@app.post("/employees")
async def create_employee(employee: Employee):
    existing = await employees_collection.find_one({"employee_id": employee.employee_id})
    if existing:
        raise HTTPException(status_code=400, detail="Employee ID already exists")
    await employees_collection.insert_one(employee.dict())
    return {"message": "Employee created successfully"}

# 2. Get Employee by ID
@app.get("/employees/{employee_id}")
async def get_employee(employee_id: str):
    employee = await employees_collection.find_one({"employee_id": employee_id})
    if not employee:
        raise HTTPException(status_code=404, detail="Employee not found")
    employee["_id"] = str(employee["_id"])
    return employee

# 3. Update Employee
@app.put("/employees/{employee_id}")
async def update_employee(employee_id: str, updates: EmployeeUpdate):
    update_data = {k: v for k, v in updates.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    result = await employees_collection.update_one({"employee_id": employee_id}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee updated successfully"}

# 4. Delete Employee
@app.delete("/employees/{employee_id}")
async def delete_employee(employee_id: str):
    result = await employees_collection.delete_one({"employee_id": employee_id})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted successfully"}

# 5. List Employees by Department
@app.get("/employees")
async def list_employees(department: str = Query(None)):
    query = {}
    if department:
        query["department"] = department
    cursor = employees_collection.find(query).sort("joining_date", -1)
    employees = []
    async for emp in cursor:
        emp["_id"] = str(emp["_id"])
        employees.append(emp)
    return employees

# 6. Average Salary by Department
@app.get("/employees/avg-salary")
async def average_salary_by_department():
    pipeline = [
        {"$group": {"_id": "$department", "avg_salary": {"$avg": "$salary"}}},
        {"$project": {"department": "$_id", "avg_salary": 1, "_id": 0}}
    ]
    cursor = employees_collection.aggregate(pipeline)
    result = []
    async for doc in cursor:
        result.append(doc)
    return result

# 7. Search Employees by Skill
@app.get("/employees/search")
async def search_by_skill(skill: str):
    cursor = employees_collection.find({"skills": skill})
    employees = []
    async for emp in cursor:
        emp["_id"] = str(emp["_id"])
        employees.append(emp)
    return employees
