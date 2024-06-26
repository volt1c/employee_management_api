from flask import request, Response, Blueprint, jsonify
from datetime import datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from src.models.schedule import Schedule

from src import db

schedules = Blueprint('schedules', __name__)


@schedules.route('/schedules', methods=['POST'])
@jwt_required()
def create_schedule():
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return Response(response=jsonify({'message': 'Unauthorized'}).data, status=403, mimetype='application/json')

    data = request.get_json()
    new_schedule = Schedule(
        employee_id=data['employee_id'],
        department_id=data['department_id'],
        work_date=datetime.strptime(data['work_date'], '%Y-%m-%d').date(),
        start_time=datetime.strptime(data['start_time'], '%H:%M:%S').time(),
        end_time=datetime.strptime(data['end_time'], '%H:%M:%S').time()
    )
    db.session.add(new_schedule)
    db.session.commit()
    return Response(response=jsonify({'message': 'Schedule created successfully'}).data, status=201,
                    mimetype='application/json')


@schedules.route('/schedules', methods=['GET'])
@jwt_required()
def get_schedules():
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return Response(response=jsonify({'message': 'Unauthorized'}).data, status=403, mimetype='application/json')

    schedules_all = Schedule.query.all()
    schedules_list = [{
        'schedule_id': sch.schedule_id,
        'employee_id': sch.employee_id,
        'department_id': sch.department_id,
        'department_name': sch.department.name,
        'work_date': sch.work_date.strftime('%Y-%m-%d'),
        'start_time': sch.start_time.strftime('%H:%M:%S'),
        'end_time': sch.end_time.strftime('%H:%M:%S')
    } for sch in schedules_all]
    return Response(response=jsonify(schedules_list).data, status=200, mimetype='application/json')


@schedules.route('/schedules/<int:schedule_id>', methods=['GET'])
@jwt_required()
def get_schedule(schedule_id):
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return Response(response=jsonify({'message': 'Unauthorized'}).data, status=403, mimetype='application/json')

    schedule = Schedule.query.get(schedule_id)
    if schedule:
        schedule_data = {
            'schedule_id': schedule.schedule_id,
            'employee_id': schedule.employee_id,
            'department_id': schedule.department_id,
            'department_name': schedule.department.name,
            'work_date': schedule.work_date.strftime('%Y-%m-%d'),
            'start_time': schedule.start_time.strftime('%H:%M:%S'),
            'end_time': schedule.end_time.strftime('%H:%M:%S')
        }
        return Response(response=jsonify(schedule_data).data, status=200, mimetype='application/json')
    return Response(response=jsonify({'message': 'Schedule not found'}).data, status=404, mimetype='application/json')


@schedules.route('/schedules/<int:schedule_id>', methods=['PUT'])
@jwt_required()
def update_schedule(schedule_id):
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return Response(response=jsonify({'message': 'Unauthorized'}).data, status=403, mimetype='application/json')

    data = request.get_json()
    schedule = Schedule.query.get(schedule_id)
    if schedule:
        schedule.employee_id = data['employee_id']
        schedule.department_id = data['department_id']
        schedule.work_date = datetime.strptime(data['work_date'], '%Y-%m-%d').date()
        schedule.start_time = datetime.strptime(data['start_time'], '%H:%M:%S').time()
        schedule.end_time = datetime.strptime(data['end_time'], '%H:%M:%S').time()
        db.session.commit()
        return Response(response=jsonify({'message': 'Schedule updated successfully'}).data, status=200,
                        mimetype='application/json')
    return Response(response=jsonify({'message': 'Schedule not found'}).data, status=404, mimetype='application/json')


@schedules.route('/schedules/<int:schedule_id>', methods=['DELETE'])
@jwt_required()
def delete_schedule(schedule_id):
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return Response(response=jsonify({'message': 'Unauthorized'}).data, status=403, mimetype='application/json')

    schedule = Schedule.query.get(schedule_id)
    if schedule:
        db.session.delete(schedule)
        db.session.commit()
        return Response(response=jsonify({'message': 'Schedule deleted successfully'}).data, status=200,
                        mimetype='application/json')
    return Response(response=jsonify({'message': 'Schedule not found'}).data, status=404, mimetype='application/json')
