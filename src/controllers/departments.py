from flask import request, Response, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from src import db
from src.models.department import Department

departments = Blueprint('departments', __name__)


@departments.route('/', methods=['POST'])
@jwt_required()
def create_department():
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return Response(response=jsonify({'message': 'Unauthorized'}).data, status=403, mimetype='application/json')

    data = request.get_json()
    new_department = Department(department_name=data['department_name'])
    db.session.add(new_department)
    db.session.commit()
    return Response(response=jsonify({'message': 'Department created successfully'}).data, status=201,
                    mimetype='application/json')


@departments.route('/', methods=['GET'])
@jwt_required()
def get_departments():
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return Response(response=jsonify({'message': 'Unauthorized'}).data, status=403, mimetype='application/json')

    departments_all = Department.query.all()
    departments_list = [
        {
            'department_id': dep.department_id,
            'department_name': dep.department_name
        } for dep in departments_all]
    return Response(response=jsonify(departments_list).data, status=200, mimetype='application/json')


@departments.route('/<int:department_id>', methods=['GET'])
@jwt_required()
def get_department(department_id):
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return Response(response=jsonify({'message': 'Unauthorized'}).data, status=403, mimetype='application/json')

    department = Department.query.get(department_id)
    if department:
        department_data = {'department_id': department.department_id, 'department_name': department.department_name}
        return Response(response=jsonify(department_data).data, status=200, mimetype='application/json')
    return Response(response=jsonify({'message': 'Department not found'}).data, status=404, mimetype='application/json')


@departments.route('/<int:department_id>', methods=['PUT'])
@jwt_required()
def update_department(department_id):
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return Response(response=jsonify({'message': 'Unauthorized'}).data, status=403, mimetype='application/json')

    data = request.get_json()
    department = Department.query.get(department_id)
    if department:
        department.department_name = data['department_name']
        db.session.commit()
        return Response(response=jsonify({'message': 'Department updated successfully'}).data, status=200,
                        mimetype='application/json')
    return Response(response=jsonify({'message': 'Department not found'}).data, status=404, mimetype='application/json')


@departments.route('/<int:department_id>', methods=['DELETE'])
@jwt_required()
def delete_department(department_id):
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return Response(response=jsonify({'message': 'Unauthorized'}).data, status=403, mimetype='application/json')

    department = Department.query.get(department_id)
    if department:
        db.session.delete(department)
        db.session.commit()
        return Response(response=jsonify({'message': 'Department deleted successfully'}).data, status=200,
                        mimetype='application/json')
    return Response(response=jsonify({'message': 'Department not found'}).data, status=404, mimetype='application/json')
