# third-party imports
from flask_restx import Resource, Namespace
from flask_jwt_extended import jwt_required

# local imports
from .. import api, db, authorizations
from ..models import Course, Student
from ..api_models import course_response_model, course_model
from ..utils import generate_response


course_ns = Namespace("Course", path="/course", description="Operations about Course", authorizations=authorizations)

@course_ns.route("")
@course_ns.doc(responses={200: "OK", 201: "Created", 400: "Bad Request", 401: "Unauthorized", 500: "Internal Server Error"}, security="jsonWebToken")
class CourseList(Resource):
  method_decorators = [jwt_required()]
  def get(self):
    """Get a list of all courses."""
    courses = Course.query.all()
    return generate_response(200, "Request processed successful", api.marshal(courses, course_response_model)), 200

  @course_ns.expect(course_model)
  def post(self):
    """Add a new course."""
    # check if the name is already in use
    existing_course_name = Course.query.filter_by(name=api.payload["name"]).first()
    if existing_course_name:
      return generate_response(400, "Name is already in use"), 400
    new_course = Course(name=api.payload["name"])

    # query for the students with the specified IDs
    associated_students = Student.query.filter(Student.id.in_(api.payload["student_ids"])).all()

    new_course.students = associated_students

    db.session.add(new_course)
    db.session.commit()
    return generate_response(201, "Course created successful", api.marshal(new_course, course_response_model)), 201

@course_ns.route("/<int:id>")
@course_ns.doc(responses={200: "OK", 204: "No Content", 400: "Bad Request", 401: "Unauthorized", 404: "Not Found", 500: "Internal Server Error"}, params={"id": "Course ID"}, security="jsonWebToken")
class CourseResource(Resource):
  method_decorators = [jwt_required()]
  def get(self, id):
    """Get course by ID."""
    course = Course.query.get(id)
    if not course:
      return generate_response(404, "Course not found"), 404
    return generate_response(200, "Request processed successful", api.marshal(course, course_response_model)), 200

  @course_ns.expect(course_model)
  def put(self, id):
    """Update courses by ID."""
    course = Course.query.get(id)
    if not course:
      return generate_response(404, "Course not found"), 404

    # check if the new name is already in use
    existing_course_name = Course.query.filter_by(name=api.payload["name"]).first()
    if existing_course_name and existing_course_name.id != id:
      return generate_response(400, "Name is already in use"), 400
    course.name = api.payload["name"]

    # update associated students
    if "student_ids" in api.payload:
      course.students = Student.query.filter(Student.id.in_(api.payload["student_ids"])).all()

    db.session.commit()
    return generate_response(200, "Course updated successful", api.marshal(course, course_response_model)), 200

  def delete(self, id):
    """Delete courses by ID."""
    course = Course.query.get(id)
    if not course:
      return generate_response(404, "Course not found"), 404

    db.session.delete(course)
    db.session.commit()
    return generate_response(204, "Course deleted successful", api.marshal(course, course_response_model)), 204