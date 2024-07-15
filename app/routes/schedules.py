from datetime import datetime
from flask import request, Blueprint, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models.schedule import Schedule

from app.database import db
from app.utils.decorators.save_log import save_log

schedules = Blueprint('schedules', __name__)


@schedules.route('/', methods=['POST'])
@jwt_required()
@save_log
def create_schedule():
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return jsonify({'message': 'Unauthorized'}), 403

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
    return jsonify({'message': 'Schedule created successfully'}), 201


@schedules.route('/', methods=['GET'])
@jwt_required()
def get_schedules():
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return jsonify({'message': 'Unauthorized'}), 403

    schedules_all = Schedule.query.all()
    schedules_list = [{
        'schedule_id': sch.schedule_id,
        'employee_id': sch.employee_id,
        'department_id': sch.department_id,
        'department_name': sch.department.department_name,
        'work_date': sch.work_date.strftime('%Y-%m-%d'),
        'start_time': sch.start_time.strftime('%H:%M:%S'),
        'end_time': sch.end_time.strftime('%H:%M:%S')
    } for sch in schedules_all]
    return jsonify(schedules_list), 200


@schedules.route('/<int:schedule_id>', methods=['GET'])
@jwt_required()
def get_schedule(schedule_id):
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return jsonify({'message': 'Unauthorized'}), 403

    schedule = Schedule.query.get(schedule_id)
    if schedule:
        schedule_data = {
            'schedule_id': schedule.schedule_id,
            'employee_id': schedule.employee_id,
            'department_id': schedule.department_id,
            'department_name': schedule.department.department_name,
            'work_date': schedule.work_date.strftime('%Y-%m-%d'),
            'start_time': schedule.start_time.strftime('%H:%M:%S'),
            'end_time': schedule.end_time.strftime('%H:%M:%S')
        }
        return jsonify(schedule_data), 200
    return jsonify({'message': 'Schedule not found'}), 404


@schedules.route('/<int:schedule_id>', methods=['PUT'])
@jwt_required()
@save_log
def update_schedule(schedule_id):
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return jsonify({'message': 'Unauthorized'}), 403

    data = request.get_json()
    schedule = Schedule.query.get(schedule_id)
    if schedule:
        schedule.employee_id = data['employee_id']
        schedule.department_id = data['department_id']
        schedule.work_date = datetime.strptime(data['work_date'], '%Y-%m-%d').date()
        schedule.start_time = datetime.strptime(data['start_time'], '%H:%M:%S').time()
        schedule.end_time = datetime.strptime(data['end_time'], '%H:%M:%S').time()
        db.session.commit()
        return jsonify({'message': 'Schedule updated successfully'}), 200
    return jsonify({'message': 'Schedule not found'}), 404


@schedules.route('/<int:schedule_id>', methods=['DELETE'])
@jwt_required()
@save_log
def delete_schedule(schedule_id):
    current_admin_id = get_jwt_identity()
    if not current_admin_id:
        return jsonify({'message': 'Unauthorized'}), 403

    schedule = Schedule.query.get(schedule_id)
    if schedule:
        db.session.delete(schedule)
        db.session.commit()
        return jsonify({'message': 'Schedule deleted successfully'}), 200
    return jsonify({'message': 'Schedule not found'}), 404
