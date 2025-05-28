from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from flask_smorest import abort,Blueprint
from flask.views import MethodView
from schemas import StoreSchema
from models import StoreModel
from flask import jsonify
from db import db

blp = Blueprint("Stores",__name__,description="operations on Stores")

@blp.route("/store")
class Stores(MethodView):

    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self,store_data):
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(400, message="Store with this name exists")
        except SQLAlchemyError:
            abort(500, message="Request unsucessfull")
        return store

    @blp.response(200,StoreSchema(many=True))
    def get(self):
        try:
            store = StoreModel.query.all()
        except SQLAlchemyError:
            abort(400, message="Request Unsucessfull")
        return store

@blp.route("/store/<string:id>")
class Store(MethodView):

    @blp.response(200,StoreSchema)
    def get(self,id):
        try:
            store = StoreModel.query.get_or_404(id)
        except SQLAlchemyError:
            abort(404,message="Store not found")
        return store
    def delete(self,id):
        try:
            store = StoreModel.query.get_or_404(id)
            if not store:
                return jsonify({"error": "Store not found"}), 404
            if store.items.count() > 0:
                return jsonify({"error": "Cannot delete store with items"}), 400
            db.session.delete(store)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message = "Bad request")
        return {"Message":"Store deleted"},200