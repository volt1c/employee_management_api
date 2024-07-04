# pylint: disable=too-few-public-methods
# pylint: disable=line-too-long
from src.database import db


class Schedule(db.Model):
    __tablename__ = 'schedules'
    schedule_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    employee_id = db.Column(db.Integer, db.ForeignKey('employees.employee_id'), nullable=False)
    department_id = db.Column(db.Integer, db.ForeignKey('departments.department_id'), nullable=False)
    work_date = db.Column(db.Date, nullable=False)
    start_time = db.Column(db.Time, nullable=False)
    end_time = db.Column(db.Time, nullable=False)
    employee = db.relationship('Employee', backref=db.backref('schedules', lazy=True))
    department = db.relationship('Department', backref=db.backref('schedules', lazy=True))
