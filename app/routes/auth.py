import os

from flask import request, Blueprint, jsonify, abort

from flask_jwt_extended import create_access_token

from app.models.admin import Admin
from app.database import db
from app.utils.decorators.save_log import save_log

# user controller blueprint to be registered with api blueprint
auth = Blueprint('auth', __name__)


# Authentication routes
@auth.route('/login', methods=['POST'])
@save_log
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    admin = Admin.query.filter_by(username=username).first()
    if admin and admin.check_password(password):
        access_token = create_access_token(identity=admin.admin_id)
        return jsonify(access_token=access_token), 200
    return jsonify({"msg": "Bad username or password"}), 401


@auth.route('/register', methods=['POST'], )
@save_log
def admin_register():
    if os.environ.get('ROUTE_ADMIN_REGISTRATION') == 'False':
        return abort(404)
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')

    admin_by_username = (Admin.query
                         .filter_by(username=username)
                         .first())
    admin_by_email = (Admin.query
                      .filter_by(email=email)
                      .first())
    if admin_by_username or admin_by_email:
        return jsonify({"msg": "Username or email already exists"}), 400

    new_admin = Admin(username=username, email=email)
    new_admin.set_password(password)
    db.session.add(new_admin)
    db.session.commit()
    return jsonify({"msg": "Admin registered successfully"}), 201
