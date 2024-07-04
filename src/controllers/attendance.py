from datetime import datetime
from flask import request, Response, jsonify, Blueprint
from src import db
from src.models.attendace import Attendance

attendance = Blueprint('attendance', __name__)


@attendance.route('/log_entry', methods=['POST'])
def log_entry():
    data = request.get_json()
    employee_id = data['employee_id']
    new_entry = Attendance(employee_id=employee_id)
    db.session.add(new_entry)
    db.session.commit()
    return Response(
        response=jsonify({'message': 'Entry logged successfully'}).data,
        status=201,
        mimetype='application/json'
    )


@attendance.route('/log_exit', methods=['POST'])
def log_exit():
    data = request.get_json()
    employee_id = data['employee_id']
    log = (Attendance.query
           .filter_by(employee_id=employee_id)
           .order_by(Attendance.entry_time.desc())
           .first())
    if log:
        if not log.exit_time:
            log.exit_time = datetime.now()
        else:
            new_exit = Attendance(employee_id=employee_id, exit_time=datetime.now())
            db.session.add(new_exit)
        db.session.commit()
        return Response(
            response=jsonify({'message': 'Exit logged successfully'}).data,
            status=200,
            mimetype='application/json'
        )
    return Response(
        response=jsonify({'message': 'No entry found for this employee'}).data,
        status=404,
        mimetype='application/json'
    )
