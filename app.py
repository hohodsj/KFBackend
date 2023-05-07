from flask import Flask
from flask_smorest import Api
from flask_cors import CORS

from resources.profile import blp as ProfileBlueprint
from resources.qna import blp as QuestionAnswerBlueprint
from resources.image import blp as ImageBlueprint
import logging
from db import db
import os

def create_app():
    logging.info('/create_app')
    app = Flask(__name__)
    CORS(app)
    app.config["API_TITLE"] = "KF Endpoints API"
    app.config["API_VERSION"] = "v1"
    app.config["OPENAPI_VERSION"] = "3.0.3"
    app.config["OPENAPI_URL_PREFIX"] = "/"
    app.config["OPENAPI_SWAGGER_UI_PATH"] = "/swagger-ui"
    app.config["OPENAPI_SWAGGER_UI_URL"] = "https://cdn.jsdelivr.net/npm/swagger-ui-dist/"
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URL" ,"sqlite:///data.db")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)
    with app.app_context():
        # create table if they don't exists
        db.create_all()

    api = Api(app)
    api.register_blueprint(ProfileBlueprint)
    api.register_blueprint(QuestionAnswerBlueprint)
    api.register_blueprint(ImageBlueprint)
    return app


# @app.route('/profile')
# def my_profile():
#     response_body = {
#         "name" : "some name",
#         "about" : "some info"
#     }
#     return response_body