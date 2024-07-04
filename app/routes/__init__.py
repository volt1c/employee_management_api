from flask import Blueprint

from app.routes.auth import auth
from app.routes.attendance import attendance
from app.routes.departments import departments
from app.routes.employees import employees
from app.routes.schedules import schedules

# main blueprint to be registered with application
api = Blueprint('api', __name__)

# register user with api blueprint
api.register_blueprint(auth, url_prefix="/auth")
api.register_blueprint(attendance, url_prefix="/attendance")
api.register_blueprint(departments, url_prefix="/departments")
api.register_blueprint(employees, url_prefix="/employees")
api.register_blueprint(schedules, url_prefix="/schedules")
