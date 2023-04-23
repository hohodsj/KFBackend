from flask import Flask

api = Flask(__name__)

@api.route('/profile')
def my_profile():
    response_body = {
        "name" : "some name",
        "about" : "some info"
    }
    return response_body