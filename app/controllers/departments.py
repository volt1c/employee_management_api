from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.database import db
from app.models.department import Department

departments = Blueprint('departments', __name__)


@departments.route('/', methods=['POST'])
@jwt_required()
def create_department():
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    new_department = Department(department_name=data['department_name'])
    db.session.add(new_department)
    db.session.commit()
    return jsonify({'message': 'Department created successfully'}), 201


@departments.route('/', methods=['GET'])
@jwt_required()
def get_departments():
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return jsonify({'message': 'Unauthorized'}), 403

    departments_all = Department.query.all()
    departments_list = [
        {
            'department_id': dep.department_id,
            'department_name': dep.department_name
        } for dep in departments_all]
    return jsonify(departments_list), 200


@departments.route('/<int:department_id>', methods=['GET'])
@jwt_required()
def get_department(department_id):
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return jsonify({'message': 'Unauthorized'}), 403

    department = Department.query.get(department_id)
    if department:
        department_data = {
            'department_id': department.department_id,
            'department_name': department.department_name
        }
        return jsonify(department_data), 200
    return jsonify({'message': 'Department not found'}), 404


@departments.route('/<int:department_id>', methods=['PUT'])
@jwt_required()
def update_department(department_id):
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    department = Department.query.get(department_id)
    if department:
        department.department_name = data['department_name']
        db.session.commit()
        return jsonify({'message': 'Department updated successfully'}), 200
    return jsonify({'message': 'Department not found'}), 404


@departments.route('/<int:department_id>', methods=['DELETE'])
@jwt_required()
def delete_department(department_id):
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return jsonify({'message': 'Unauthorized'}), 403

    department = Department.query.get(department_id)
    if department:
        db.session.delete(department)
        db.session.commit()
        return jsonify({'message': 'Department deleted successfully'}), 200
    return jsonify({'message': 'Department not found'}), 404
