# third-party imports
from flask_restx import Resource
from flask_jwt_extended import jwt_required, create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

# local imports
from . import api, db, auth, course, student
from .models import User, Course, Student


# data model for request and response documents
from .api_models import user_response_model, user_model, course_response_model, course_model, student_response_model, student_model


@auth.route("/register")
class Register(Resource):
  @auth.expect(user_model)
  @auth.marshal_with(user_response_model, code=201)
  def post(self):
    """Register an account."""
    user = User(username=auth.payload["username"], password=generate_password_hash(auth.payload["password"]))
    db.session.add(user)
    db.session.commit()
    return user, 201

@auth.route("/login")
class Login(Resource):
  @auth.expect(user_model)
  def post(self):
    """Login account."""
    user = User.query.filter_by(username=auth.payload["username"]).first()
    if not user:
      api.abort(401, "User does not exist")
    if not check_password_hash(user.password, auth.payload["password"]):
      api.abort(401, "Incorrect password")

    if user.token is not None:
      return {"access_token": user.token}

    access_token = create_access_token(user.username)

    user.token = access_token
    db.session.commit()

    return {"access_token": access_token}

@course.route("")
@course.doc(security="jsonWebToken")
class CourseList(Resource):
  method_decorators = [jwt_required()]

  @course.marshal_list_with(course_response_model)
  def get(self):
    """Get a list of all courses."""
    courses = Course.query.all()
    return courses

  @course.expect(course_model)
  @course.marshal_with(course_response_model, code=201)
  def post(self):
    """Add a new course."""
    new_course = Course(**api.payload)
    db.session.add(new_course)
    db.session.commit()
    return new_course, 201

@course.route("/<int:course_id>")
@course.doc(responses={404: "Course not found"}, params={"course_id": "Course ID"}, security="jsonWebToken")
class CourseResource(Resource):
  method_decorators = [jwt_required()]

  @course.marshal_with(course_response_model)
  def get(self, course_id):
    """Get course details by ID."""
    course = Course.query.get(course_id)
    if not course:
      api.abort(404, "Course with ID {} not found".format(course_id))
    return course

  @course.expect(course_model)
  @course.marshal_with(course_response_model)
  def put(self, course_id):
    """Update courses by ID."""
    course = Course.query.get(course_id)
    if not course:
      api.abort(404, "Course with ID {} not found".format(course_id))

    if "name" in api.payload:
      course.name = api.payload["name"]

    db.session.commit()
    return course

  @course.doc(responses={204: "Course deleted"})
  def delete(self, course_id):
    """Delete courses by ID."""
    course = Course.query.get(course_id)
    if not course:
      api.abort(404, "Course with ID {} not found".format(course_id))
    db.session.delete(course)
    db.session.commit()
    return "", 204

@student.route("")
@student.doc(security="jsonWebToken")
class StudentList(Resource):
  method_decorators = [jwt_required()]

  @student.marshal_list_with(student_response_model)
  def get(self):
    """Get a list of all students."""
    students = Course.query.all()
    return students

  @student.expect(student_model)
  @student.marshal_with(student_response_model, code=201)
  def post(self):
    """Add a new student."""
    new_student = Student(**api.payload)
    db.session.add(new_student)
    db.session.commit()
    return new_student, 201

@student.route("/<int:student_id>")
@student.doc(responses={404: "Student not found"}, params={"student_id": "Student ID"}, security="jsonWebToken")
class StudentResource(Resource):
  method_decorators = [jwt_required()]

  @student.marshal_with(student_response_model)
  def get(self, student_id):
    """Get student details by ID."""
    student = Student.query.get(student_id)
    if not student:
      api.abort(404, "Student with ID {} not found".format(student_id))
    return student

  @student.expect(student_model)
  @student.marshal_with(student_response_model)
  def put(self, student_id):
    """Update students by ID."""
    student = Student.query.get(student_id)
    if not student:
      api.abort(404, "Student with ID {} not found".format(student_id))

    if "name" in api.payload:
      student.name = api.payload["name"]

    db.session.commit()
    return student

  @student.doc(responses={204: "Student deleted"})
  def delete(self, student_id):
    """Delete students by ID."""
    student = Student.query.get(student_id)
    if not student:
      api.abort(404, "Student with ID {} not found".format(student_id))
    db.session.delete(student)
    db.session.commit()
    return "", 204