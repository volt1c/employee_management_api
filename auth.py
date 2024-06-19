from flask import request
from flask_jwt_extended import JWTManager, create_access_token, jwt_required
from flask_restful import Resource


def init_auth(app):
    app.config['JWT_SECRET_KEY'] = 'your_jwt_secret_key'
    jwt = JWTManager(app)


class AuthResource(Resource):
    def post(self):
        data = request.get_json()
        # todo: add users
        if data['username'] == 'admin' and data['password'] == 'password':
            access_token = create_access_token(identity={'username': data['username']})
            return {'access_token': access_token}, 200
        return {'message': 'Invalid credentials'}, 401
