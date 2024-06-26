from flask import request, Response, Blueprint, jsonify
from datetime import datetime
from flask_jwt_extended import jwt_required

from src import db
from src.models.employee import Employee


employees = Blueprint('employees', __name__)


@employees.route('/', methods=['POST'])
@jwt_required()
def create_employee():
    data = request.get_json()
    new_employee = Employee(
        first_name=data['first_name'],
        last_name=data['last_name'],
        position=data['position'],
        email=data['email'],
        phone=data['phone'],
        date_of_joining=datetime.strptime(data['date_of_joining'], '%Y-%m-%d')
    )
    db.session.add(new_employee)
    db.session.commit()
    return Response(
        response=jsonify({'message': 'Employee created successfully'}).data,
        status=201,
        mimetype='application/json'
    )


@employees.route('/', methods=['GET'])
@jwt_required()
def get_employees():
    employees_all = Employee.query.all()
    employees_list = [{
        'employee_id': emp.employee_id,
        'first_name': emp.first_name,
        'last_name': emp.last_name,
        'position': emp.position,
        'email': emp.email,
        'phone': emp.phone,
        'date_of_joining': emp.date_of_joining.strftime('%Y-%m-%d')
    } for emp in employees_all]
    return Response(
        response=jsonify(employees_list).data,
        status=200,
        mimetype='application/json'
    )


@employees.route('/<int:employee_id>', methods=['GET'])
@jwt_required()
def get_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if employee:
        employee_data = {
            'employee_id': employee.employee_id,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'position': employee.position,
            'email': employee.email,
            'phone': employee.phone,
            'date_of_joining': employee.date_of_joining.strftime('%Y-%m-%d')
        }
        return Response(response=jsonify(employee_data).data, status=200, mimetype='application/json')
    return Response(response=jsonify({'message': 'Employee not found'}).data, status=404, mimetype='application/json')


@employees.route('/<int:employee_id>', methods=['PUT'])
@jwt_required()
def update_employee(employee_id):
    data = request.get_json()
    employee = Employee.query.get(employee_id)
    if employee:
        employee.first_name = data['first_name']
        employee.last_name = data['last_name']
        employee.position = data['position']
        employee.email = data['email']
        employee.phone = data['phone']
        employee.date_of_joining = datetime.strptime(data['date_of_joining'], '%Y-%m-%d')
        db.session.commit()
        return Response(
            response=jsonify({'message': 'Employee updated successfully'}).data,
            status=200,
            mimetype='application/json'
        )
    return Response(response=jsonify({'message': 'Employee not found'}).data, status=404, mimetype='application/json')


@employees.route('/<int:employee_id>', methods=['DELETE'])
@jwt_required()
def delete_employee(employee_id):
    employee = Employee.query.get(employee_id)
    if employee:
        db.session.delete(employee)
        db.session.commit()
        return Response(
            response=jsonify({'message': 'Employee deleted successfully'}).data,
            status=200,
            mimetype='application/json'
        )
    return Response(response=jsonify({'message': 'Employee not found'}).data, status=404, mimetype='application/json')
