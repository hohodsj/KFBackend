from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import SQLAlchemyError, IntegrityError

from schemas import ImageSchema
from db import db
from models import ImageModel
import requests
import os

blp= Blueprint("Images", __name__, description="Operations on images")

def send_email(subject, body):
    to = []
    user1_email = os.getenv("USER1_EMAIL")
    if user1_email:
        to.append(user1_email)
    if os.getenv("USER2_EMAIL"):
        to.append(os.getenv("USER2_EMAIL"))
    domain = os.getenv("MAILGUN_DOMAIN")
    api = os.getenv("MAILGUN_API_KEY")
    print(f'domain:{domain}  api:{api} subject:{subject} body:{body}')
    if os.getenv("IS_SEND", 'False') == 'True':
        requests.post(
            f'https://api.mailgun.net/v3/{domain}/messages',
            auth=("api", api),
            data={"from": f'kethsclurb.onrender <mailgun@{domain}>',
                "to": [to],
                "subject": subject,
                "text": body})
    
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
            abort(409, message=f"Image already exists")
        except SQLAlchemyError:
            abort(500, message=f"An error occurred while inserting the image")
        return image_obj
    
    @blp.response(200, ImageSchema(many=True))
    def get(self):
        return ImageModel.query.all()

@blp.route("/image/<int:image_id>")
class Image(MethodView):
    @blp.response(200, ImageSchema)
    def get(self, image_id):
        image = ImageModel.query.get_or_404(image_id)
        if image_id == 1:
            send_email("Page Kathleen just landed!", "Kathleen just landed on the website")
        elif image_id == 2:
            send_email("Page Kathleen start to answer questions", "Questions")
        elif image_id == 4:
            send_email("Page Kathleen got the reward!", "Done")
        return image
