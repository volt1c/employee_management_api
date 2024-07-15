from datetime import datetime
from flask import request, jsonify, Blueprint
from app.database import db
from app.models.attendace import Attendance
from app.utils.decorators.emit_preview import emit_preview

attendance = Blueprint('attendance', __name__)


@attendance.route('/report/entry', methods=['POST'])
@emit_preview
def report_entry():
    data = request.get_json()
    employee_id = data['employee_id']
    new_entry = Attendance(employee_id=employee_id)
    db.session.add(new_entry)
    db.session.commit()
    return jsonify({'message': 'Entry logged successfully'}), 201


@attendance.route('/report/exit', methods=['POST'])
@emit_preview
def report_exit():
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
        return jsonify({'message': 'Exit logged successfully'}), 200
    return jsonify({'message': 'No entry found for this employee'}), 404
