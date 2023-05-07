from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from schemas import ImageSchema
from db import db
from models import ImageModel

blp= Blueprint("Images", __name__, description="Operations on images")

@blp.route("/images")
class Image(MethodView):
    @blp.arguments(ImageSchema)
    @blp.response(200, ImageSchema)
    def post(self, image_data):
        image_obj = ImageModel.query.get(image_data["id"]) if "id" in image_data else ImageModel(**image_data)
        if image_obj:
            image_obj.url = image_data["url"]
            image_obj.name = image_data["name"]
        try:
            db.session.add(image_obj)
            db.session.commit()
        except IntegrityError:
            abort(409, message="Image already exists")
        except SQLAlchemyError:
            abort(500, message="An error occurred while inserting the image")
        return image_obj
    
    @blp.response(200, ImageSchema(many=True))
    def get(self):
        return ImageModel.query.all()

@blp.route("/image/<int:image_id>")
class Image(MethodView):
    @blp.response(200, ImageSchema)
    def get(self, image_id):
        image = ImageModel.query.get_or_404(image_id)
        return image
