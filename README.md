Employee API - FastAPI & MongoDB

A simple Employee Management API built with FastAPI and MongoDB.
Provides CRUD operations, search, and aggregation endpoints for managing employee data.

Features

⦁	Create Employee (POST /employees)
⦁	Insert a new employee. employee_id must be unique.

⦁	Get Employee by ID (GET /employees/{employee_id})
⦁	Retrieve employee details by ID. Returns 404 if not found.

⦁	Update Employee (PUT /employees/{employee_id})
⦁	Update existing employee details. Supports partial updates.

⦁	Delete Employee (DELETE /employees/{employee_id})
⦁	Delete an employee record.

⦁	List Employees by Department (GET /employees?department=XYZ)
⦁	List employees in a department, sorted by joining_date (newest first).

⦁	Average Salary by Department (GET /employees/avg-salary)
⦁	Computes average salary per department using MongoDB aggregation.

⦁	Search Employees by Skill (GET /employees/search?skill=XYZ)
⦁	Find employees with a specific skill.

Technologies Used

⦁	Python 3.13+
⦁	FastAPI – Web framework
⦁	MongoDB – Local database
⦁	Motor – Async MongoDB driver
⦁	Pydantic – Data validation

Setup Instructions

Install Dependencies
⦁	pip install fastapi uvicorn motor pymongo pydantic
⦁	Start MongoDB
⦁	Make sure MongoDB service is running:
⦁	net start MongoDB
 Run the FastAPI App
⦁	uvicorn main:app --reload

API URL: http://127.0.0.1:8000/
Swagger UI: http://127.0.0.1:8000/docs

Notes:
⦁	MongoDB unique index ensures employee_id uniqueness.
⦁	Dates are stored as ISO strings (YYYY-MM-DD).
⦁	Swagger UI is recommended for interactive testing.
