# third-party imports
from flask_restx import fields

# local imports
from . import api


register_response_model = api.model("Register Response", {
  "id": fields.Integer(description="User ID"),
  "username": fields.String(description="User Username"),
  "email": fields.String(description="User Email")
})

login_response_model = api.model("Login Response", {
  "token": fields.String(description="User Token")
})

student_response_model = api.model("Student Response", {
  "id": fields.Integer(description="Student ID"),
  "name": fields.String(description="Student Name"),
  "courses": fields.List(fields.Nested(api.model("Nested Course", {
    "id": fields.Integer(description="Course ID"),
    "name": fields.String(description="Course Name")
  })))
})

course_response_model = api.model("Course Response", {
  "id": fields.Integer(description="Course ID"),
  "name": fields.String(description="Course Name"),
  "students": fields.List(fields.Nested(api.model("Nested Student", {
    "id": fields.Integer(description="Student ID"),
    "name": fields.String(description="Student Name")
  })))
})

register_model = api.model("Register", {
  "username": fields.String(required=True, description="User Username"),
  "email": fields.String(required=True, description="User Email"),
  "password": fields.String(required=True, description="User password")
})

login_model = api.model("Login", {
  "username": fields.String(required=True, description="User Username"),
  "password": fields.String(required=True, description="User password")
})

student_model = api.model("Student", {
  "name": fields.String(required=True, description="Student Name")
})


course_model = api.model("Course", {
  "name": fields.String(required=True, description="Course Name"),
  "student_ids": fields.List(fields.Integer(required=False, description="Student IDs"))
})