# third-party imports
import json
from flask import Flask
from flask_restx import Api
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

def create_app(config=DevelopmentConfig):
  app = Flask(__name__)
  app.config.from_object(config)

  api.init_app(app, version="1.0", title="Course API", description="A course API")
  db.init_app(app)
  jwt.init_app(app)

  from .resources import auth_ns, student_ns, course_ns
  api.add_namespace(auth_ns)
  api.add_namespace(student_ns)
  api.add_namespace(course_ns)

  @jwt.unauthorized_loader
  def custom_error_message(callback):
    response = {
      "status": 401,
      "message": "Unauthorized access",
      "data": None
    }
    return json.dumps(response), 401, {"Content-Type": "application/json"}

  with app.app_context():
    db.create_all()

  return app