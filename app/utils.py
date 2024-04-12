# third-party imports
from flask import current_app


# function to generate output response
def generate_response(status, message, data=None):
  with current_app.app_context():
    response = {
      "status": status,
      "message": message,
      "data": data
    }
    return response