# local imports
from . import db


student_course_association = db.Table(
  "student_course_association",
  db.Column("student_id", db.Integer, db.ForeignKey("student.id")),
  db.Column("course_id", db.Integer, db.ForeignKey("course.id"))
)

class User(db.Model):
  __tablename__ = "user"

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), nullable=False, unique=True)
  email = db.Column(db.String(128), nullable=False, unique=True)
  password = db.Column(db.String(128), nullable=False)
  token = db.Column(db.String(300), nullable=True)

class Student(db.Model):
  __tablename__ = "student"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False, unique=True)
  courses = db.relationship("Course", secondary=student_course_association, back_populates="students")

class Course(db.Model):
  __tablename__ = "course"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False, unique=True)
  students = db.relationship("Student", secondary=student_course_association, back_populates="courses")