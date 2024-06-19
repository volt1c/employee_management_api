from flask import request
from flask_restful import Resource
from models import Schedule
from datetime import datetime

class ScheduleResource(Resource):
    def get(self, employee_id):
        schedules = Schedule.get_by_employee_id(employee_id)
        return {'schedules': schedules}, 200

    def post(self):
        data = request.get_json()
        entry_time = datetime.now()
        Schedule.add_entry(data['employee_id'], entry_time)
        return {'message': 'Entry recorded'}, 201

    def put(self, schedule_id):
        data = request.get_json()
        exit_time = datetime.now()
        Schedule.add_exit(schedule_id, exit_time)
        return {'message': 'Exit recorded'}, 200
