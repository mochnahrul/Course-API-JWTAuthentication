# third-party imports
from flask_restx import Resource, Namespace
from flask_jwt_extended import create_access_token
from werkzeug.security import generate_password_hash, check_password_hash

# local imports
from .. import api, db, authorizations
from ..models import User
from ..api_models import register_response_model, login_response_model, register_model, login_model


auth_ns = Namespace("Auth", path="/auth", description="Operations about Auth", authorizations=authorizations)

@auth_ns.route("/register")
class Register(Resource):
  @auth_ns.expect(register_model)
  @auth_ns.marshal_with(register_response_model, code=201)
  def post(self):
    """Create an account."""
    # check if the username is already in use
    existing_user_username = User.query.filter_by(username=api.payload["username"]).first()
    if existing_user_username:
      api.abort(400, "Username is already in use")

    # check if the email is already in use
    existing_user_email = User.query.filter_by(email=api.payload["email"]).first()
    if existing_user_email:
      api.abort(400, "Email is already in use")

    # hash the password
    api.payload["password"] = generate_password_hash(api.payload["password"])

    new_user = User(**api.payload)
    db.session.add(new_user)
    db.session.commit()
    return new_user, 201

@auth_ns.route("/login")
class Login(Resource):
  @auth_ns.expect(login_model)
  @auth_ns.marshal_with(login_response_model, code=201)
  def post(self):
    """Log in to get an access token."""
    user = User.query.filter_by(username=api.payload["username"]).first()
    if not user:
      api.abort(401, "User does not exist")
    if not check_password_hash(user.password, api.payload["password"]):
      api.abort(401, "Incorrect password")

    access_token = create_access_token(user.username)
    user.token = "Bearer " + access_token

    db.session.commit()
    return user, 201