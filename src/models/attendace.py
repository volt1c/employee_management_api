# pylint: disable=too-few-public-methods
from _datetime import datetime
from src.database import db


class Attendance(db.Model):
    __tablename__ = 'attendance'
    log_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)
    entry_time = db.Column(db.DateTime, nullable=False, default=datetime.now)
    exit_time = db.Column(db.DateTime)
    employee = db.relationship('Employee', backref=db.backref('attendance_logs', lazy=True))
