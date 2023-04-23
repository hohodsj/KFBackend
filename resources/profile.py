from flask.views import MethodView
from flask_smorest import Blueprint, abort
from schemas import ProfileSchema
import logging

blp = Blueprint("Profiles", __name__, description="Operation on profiles")

@blp.route("/profile")
class Profile(MethodView):
    @blp.response(200, ProfileSchema)
    def get(self):
        print('/profile')
        logging.info('/profile')
        response_body = {
            "name" : "some name",
            "about" : "some info"
        }
        return response_body
