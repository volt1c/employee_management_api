import os

from flask import request, Response, Blueprint, jsonify, abort

from flask_jwt_extended import create_access_token

from src.models.admin import Admin
from src import db

# user controller blueprint to be registered with api blueprint
auth = Blueprint('auth', __name__)


# Authentication routes
@auth.route('/login', methods=['POST'])
def admin_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    admin = Admin.query.filter_by(username=username).first()
    if admin and admin.check_password(password):
        access_token = create_access_token(identity=admin.admin_id)
        return Response(
            response=jsonify(access_token=access_token).data,
            status=200,
            mimetype='application/json'
        )
    return Response(
        response=jsonify({"msg": "Bad username or password"}).data,
        status=401,
        mimetype='application/json'
    )


@auth.route('/register', methods=['POST'], )
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
        return Response(
            response=jsonify({"msg": "Username or email already exists"}).data,
            status=400,
            mimetype='application/json'
        )

    new_admin = Admin(username=username, email=email)
    new_admin.set_password(password)
    db.session.add(new_admin)
    db.session.commit()
    return Response(
        response=jsonify({"msg": "Admin registered successfully"}).data,
        status=201,
        mimetype='application/json'
    )
