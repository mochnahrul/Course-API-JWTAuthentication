# third-party imports
from flask_restx import fields

# local imports
from . import api


user_response_model = api.model("UserResponse", {
  "id": fields.Integer(readonly=True, description="User ID"),
  "username": fields.String(required=True, description="Username")
})

user_model = api.model("User", {
  "username": fields.String(required=True, description="Username"),
  "password": fields.String(required=True, description="Password")
})

student_response_model = api.model("StudentResponse", {
  "id": fields.Integer(readonly=True, description="Student ID"),
  "name": fields.String(required=True, description="Student Name"),
  # "course": fields.Nested(course_response_model)
})

student_model = api.model("Student", {
  "id": fields.Integer(readonly=True, description="Student ID"),
  "name": fields.String(required=True, description="Student Name"),
  "course_id": fields.Integer(required=True, description="Course ID"),
})

course_response_model = api.model("CourseResponse", {
  "id": fields.Integer(readonly=True, description="Course ID"),
  "name": fields.String(required=True, description="Course Name"),
  "students": fields.List(fields.Nested(student_response_model))
})

course_model = api.model("Course", {
  "id": fields.Integer(readonly=True, description="Course ID"),
  "name": fields.String(required=True, description="Course Name"),
})