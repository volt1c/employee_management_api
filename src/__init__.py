import os
from flask import Flask
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt

from src.config.config import Config
from src.routes import api

load_dotenv()

app = Flask(__name__)

config = Config().dev_config

app.env = config.ENV

json_sort_keys = os.environ.get('JSON_SORT_KEYS')
app.json.sort_keys = json_sort_keys == 'True'
app.config['JSON_SORT_KEYS'] = json_sort_keys
app.secret_key = os.environ.get("SECRET_KEY")
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("SQLALCHEMY_DATABASE_URI_DEV")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.environ.get("SQLALCHEMY_TRACK_MODIFICATIONS")
app.config['JWT_SECRET_KEY'] = os.environ.get("JWT_SECRET_KEY")

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
jwt = JWTManager(app)

app.register_blueprint(api, url_prefix="/api")

# import models to let the migrate tool know

with app.app_context():
    db.create_all()
