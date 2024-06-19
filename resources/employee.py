from flask import request
from flask_restful import Resource
from models import Employee

class EmployeeResource(Resource):
    def get(self, employee_id=None):
        if employee_id:
            employee = Employee.get_by_id(employee_id)
            return {'employee': employee}, 200
        else:
            employees = Employee.get_all()
            return {'employees': employees}, 200

    def post(self):
        data = request.get_json()
        Employee.add(data['name'], data['email'])
        return {'message': 'Employee added'}, 201
