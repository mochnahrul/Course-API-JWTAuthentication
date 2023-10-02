# third-party imports
from flask import Flask
from flask_restx import Api, Namespace
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager

# local imports
from .config import DevelopmentConfig


api = Api()
db = SQLAlchemy()
jwt = JWTManager()

authorizations = {
  "jsonWebToken": {
    "type": "apiKey",
    "in": "header",
    "name": "Authorization"
  }
}

auth = Namespace("auth", description="Auth-related operations", authorizations=authorizations)
course = Namespace("courses", description="Course-related operations", authorizations=authorizations)
student = Namespace("students", description="Student-related operations", authorizations=authorizations)

def create_app(config=DevelopmentConfig):
  app = Flask(__name__)
  app.config.from_object(config)

  api.init_app(app, version="1.0", title="Course API", description="A course API")
  db.init_app(app)
  jwt.init_app(app)

  from . import resources

  api.add_namespace(auth)
  api.add_namespace(course)
  api.add_namespace(student)

  with app.app_context():
    db.create_all()

  return app