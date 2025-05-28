from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from flask_smorest import abort,Blueprint
from flask.views import MethodView
from schemas import ItemSchema,ItemUpdateSchema
from db import db
from models import ItemModel,StoreModel
from flask_jwt_extended import jwt_required

blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item")
class ItemList(MethodView):

    @jwt_required()
    @blp.arguments(ItemSchema)
    @blp.response(200,ItemSchema)
    def post(self,item_data):
        item = ItemModel(**item_data)
        try:
            if not StoreModel.query.get(item_data["store_id"]):
                abort(404, message="Store not found")
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "Same name exists")
        except SQLAlchemyError:
            abort(500,message="Item not created")
        return item

    @jwt_required()
    @blp.response(200,ItemSchema(many=True))
    def get(self):
        try:
            return ItemModel.query.all()
        except KeyError:
            abort(400,"Bad Request")

@blp.route("/item/<string:id>")
class Item(MethodView):

    @jwt_required()
    @blp.response(200,ItemSchema)
    def get(self,id):
        try:
            item = ItemModel.query.get_or_404(id)
        except SQLAlchemyError:
            abort(404,message="Request Unsuccessfull") 
        return item

    @blp.arguments(ItemUpdateSchema)
    @blp.response(201,ItemSchema)
    def put(self,item_data, id):
        item = ItemModel.query.get_or_404(id)
        try:
            item.name = item_data["name"]
            item.price = item_data["price"]
            db.session.add(item)
            db.session.commit()
        except IntegrityError:
            abort(400, message = "Bad Request")
        except SQLAlchemyError:
            abort(500, message="Item not found.")
        return item
    
    @jwt_required()
    def delete(self, id):
        item = ItemModel.query.get_or_404(id)
        if not item.tags:
            db.session.delete(item)
            db.session.commit()
            return {"message": "item deleted."}
        abort(
            400,
            message="Could not delete tag. Make sure tag is not associated with any items, then try again.",
        )