from flask import Flask
from flask_restful import Api
from db import init_db
from auth import init_auth, AuthResource
from resources.employee import EmployeeResource
from resources.schedule import ScheduleResource

app = Flask(__name__)
api = Api(app)

init_db(app)
init_auth(app)

api.add_resource(AuthResource, '/auth')
api.add_resource(EmployeeResource, '/employees', '/employees/<int:employee_id>')
api.add_resource(ScheduleResource, '/schedules/<int:employee_id>', '/schedules', '/schedules/<int:schedule_id>')

if __name__ == '__main__':
    app.run(debug=True)
