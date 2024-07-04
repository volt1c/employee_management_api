import os
from dotenv import load_dotenv
from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from app.database import db
from app.routes import api

load_dotenv()

app = Flask(__name__)

# Config
app.env = os.environ.get('ENV')
app.secret_key = os.environ.get('SECRET_KEY')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI_DEV")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = os.environ.get('SQLALCHEMY_TRACK_MODIFICATIONS')
app.config['JWT_SECRET_KEY'] = os.environ.get('JWT_SECRET_KEY')

# Don't sort keys
app.json.sort_keys = False
app.config['JSON_SORT_KEYS'] = False

db.init_app(app)
bcrypt = Bcrypt(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

app.register_blueprint(api, url_prefix="/api")

with app.app_context():
    db.create_all()
