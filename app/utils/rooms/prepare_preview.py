from datetime import date

from app.database import db
from app.models.attendace import Attendance
from app.models.employee import Employee
from app.models.schedule import Schedule


def prepare_preview(data):
    page = data['page']
    amount_employees = data['amount']
    department_id = None
    if 'department_id' in data:
        department_id = data['department_id']

    # Calculate the offset for pagination
    offset = page * amount_employees

    # Get today's date
    today = date.today()

    # Base query to get employees who are scheduled today
    employees_query = db.session.query(Employee).join(Schedule).filter(Schedule.work_date == today)

    # If department_id is specified, add it to the query
    if department_id:
        employees_query = employees_query.filter(Schedule.department_id == department_id)

    # Apply pagination
    employees_paginated = employees_query.offset(offset).limit(amount_employees).all()

    response_data = {
        "page": page,
        "present_employees": 0,
        "employees": []
    }

    for employee in employees_paginated:
        schedule = (db.session.query(Schedule)
                    .filter(
            Schedule.employee_id == employee.employee_id,
            Schedule.work_date == today).first())
        is_present = (db.session.query(Attendance)
                      .filter(
            Attendance.employee_id == employee.employee_id,
            Attendance.exit_time.is_(None)).count() > 0)

        if is_present:
            response_data["present_employees"] += 1

        response_data["employees"].append({
            "first_name": employee.first_name,
            "last_name": employee.last_name,
            "schedule": {
                "start": schedule.start_time.strftime("%H:%M:%S"),
                "end": schedule.end_time.strftime("%H:%M:%S")
            },
            "is_present": is_present
        })

    return response_data
