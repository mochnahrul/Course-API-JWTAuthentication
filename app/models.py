# local imports
from . import db


class User(db.Model):
  __tablename__ = "user"

  id = db.Column(db.Integer, primary_key=True)
  username = db.Column(db.String(20), nullable=False, unique=True)
  password = db.Column(db.String(128), nullable=False)
  token = db.Column(db.String(300), nullable=True)

class Course(db.Model):
  __tablename__ = "course"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False, unique=True)
  students = db.relationship("Student", back_populates="course")

class Student(db.Model):
  __tablename__ = "student"

  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(128), nullable=False, unique=True)
  course_id = db.Column(db.Integer, db.ForeignKey("course.id"), nullable=False)
  course = db.relationship("Course", back_populates="students")