# third-party imports
from flask_restx import Resource, Namespace
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

# local imports
from .. import api, db, authorizations
from ..models import User
from ..api_models import register_response_model, login_response_model, register_model, login_model
from ..utils import generate_response


auth_ns = Namespace("Auth", path="/auth", description="Operations about Auth", authorizations=authorizations)

@auth_ns.route("/register")
@api.doc(responses={201: "Created", 400: "Bad Request"})
class Register(Resource):
  @auth_ns.expect(register_model)
  def post(self):
    """Create an account."""
    # check if the username is already registered
    existing_user_username = User.query.filter_by(username=api.payload["username"]).first()
    if existing_user_username:
      return generate_response(400, "Username is already registered"), 400
    # check if the email is already registered
    existing_user_email = User.query.filter_by(email=api.payload["email"]).first()
    if existing_user_email:
      return generate_response(400, "Email is already registered"), 400

    # hash the password
    api.payload["password"] = generate_password_hash(api.payload["password"])

    new_user = User(**api.payload)
    db.session.add(new_user)
    db.session.commit()
    return generate_response(201, "Account created successful", api.marshal(new_user, register_response_model)), 201

@auth_ns.route("/login")
@api.doc(responses={200: "OK", 400: "Bad Request", 401: "Unauthorized"})
class Login(Resource):
  @auth_ns.expect(login_model)
  def post(self):
    """Log in to your account."""
    user = User.query.filter_by(username=api.payload["username"]).first()
    if not user:
      return generate_response(401, "Username is not registered"), 401
    if not check_password_hash(user.password, api.payload["password"]):
      return generate_response(401, "Incorrect password"), 401

    access_token = create_access_token(user.username)
    user.token = "Bearer " + access_token

    db.session.commit()
    return generate_response(200, "Login successful", api.marshal(user, login_response_model)), 200