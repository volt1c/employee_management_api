from flask import Blueprint

from app.controllers.auth import auth
from app.controllers.attendance import attendance
from app.controllers.departments import departments
from app.controllers.employees import employees
from app.controllers.schedules import schedules

# main blueprint to be registered with application
api = Blueprint('api', __name__)

# register user with api blueprint
api.register_blueprint(auth, url_prefix="/auth")
api.register_blueprint(attendance, url_prefix="/attendance")
api.register_blueprint(departments, url_prefix="/departments")
api.register_blueprint(employees, url_prefix="/employees")
api.register_blueprint(schedules, url_prefix="/schedules")
