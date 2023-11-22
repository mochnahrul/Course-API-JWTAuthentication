# third-party imports
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

# local imports
from .. import api, db, authorizations
from ..models import Student
from ..api_models import student_response_model, student_model


student_ns = Namespace("Student", path="/student", description="Operations about Student", authorizations=authorizations)

@student_ns.route("")
@student_ns.doc(security="jsonWebToken")
class StudentList(Resource):
  method_decorators = [jwt_required()]
  @student_ns.marshal_list_with(student_response_model)
  def get(self):
    """Get a list of all students."""
    students = Student.query.all()
    return students

  @student_ns.expect(student_model)
  @student_ns.marshal_with(student_response_model, code=201)
  def post(self):
    """Add a new student."""
    # check if the name is already in use
    existing_student_name = Student.query.filter_by(name=api.payload["name"]).first()
    if existing_student_name:
      api.abort(400, "Name is already in use")

    new_student = Student(**api.payload)
    db.session.add(new_student)
    db.session.commit()
    return new_student, 201

@student_ns.route("/<int:id>")
@student_ns.doc(responses={404: "Student not found"}, params={"id": "Student ID"}, security="jsonWebToken")
class StudentResource(Resource):
  method_decorators = [jwt_required()]
  @student_ns.marshal_with(student_response_model)
  def get(self, id):
    """Get student details by ID."""
    student = Student.query.get(id)
    if not student:
      api.abort(404, "Student with ID {} not found".format(id))
    return student

  @student_ns.expect(student_model)
  @student_ns.marshal_with(student_response_model)
  def put(self, id):
    """Update students by ID."""
    student = Student.query.get(id)
    if not student:
      api.abort(404, "Student with ID {} not found".format(id))

    # check if the new name is already in use
    existing_student_name = Student.query.filter_by(name=api.payload["name"]).first()
    if existing_student_name and existing_student_name.id != id:
      api.abort(400, "Name is already in use")
    student.name = api.payload["name"]

    db.session.commit()
    return student

  def delete(self, id):
    """Delete students by ID."""
    student = Student.query.get(id)
    if not student:
      api.abort(404, "Student with ID {} not found".format(id))
    db.session.delete(student)
    db.session.commit()
    return "", 204