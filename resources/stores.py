from flask_smorest import abort,Blueprint
from flask.views import MethodView
from schemas import StoreSchema
import uuid
from db import stores

blp = Blueprint("Users",__name__,description="operations on users")

@blp.route("/store")
class Stores(MethodView):

    @blp.arguments(StoreSchema)
    @blp.response(201,StoreSchema)
    def post(self,store_data):
        try:
            store_id = uuid.uuid4().hex
            store = {**store_data,"store_id":store_id}
            stores[store_id] = store
            return store, 201
        except KeyError:
            abort(400, message="Request unsucessfull")

    @blp.response(200,StoreSchema)
    def get(self):
        try:
            return stores.values(), 200
        except KeyError:
            abort(400, message="Request Unsucessfull")

@blp.route("/store/<string:id>")
class Store(MethodView):

    @blp.response(200,StoreSchema)
    def get(self,id):
        try:
            return stores[id], 200
        except KeyError:
            abort(404,message="Store not found")
        
    def delete(self,id):
        try:
            del stores[id]
            return {"message" : "Store deleted"}, 200
        except KeyError:
            abort(404, message="Store doesgvkgvjnt found") 