from flask_smorest import abort,Blueprint
from flask.views import MethodView
from schemas import ItemSchema,ItemUpdateSchema
from db import items

blp = Blueprint("items", __name__, description="Operations on items")

@blp.route("/item")
class ItemList(MethodView):

    @blp.arguments(ItemSchema)
    @blp.response(201,ItemSchema)
    def post(self,item_data):
        try:
            item_id = str(len(items) + 1)
            item = {**item_data,"id":item_id}
            items[item_id] = item
            return item
        except KeyError:
            abort(400,message="Item not created")

    @blp.response(200,ItemSchema(many=True))
    def get(self):
        try:
            return list(items.values())
        except KeyError:
            abort(400,"Bad Request")

@blp.route("/item/<string:id>")
class Item(MethodView):

    @blp.response(200,ItemSchema)
    def get(self,id):
        try:
            return items[id]
        except KeyError:
            abort(404,message="Request Unsuccessfull") 

    @blp.arguments(ItemUpdateSchema)
    @blp.response(201,ItemSchema)
    def put(self,item_data, id):
        try:
            item = items[id]
            item |= item_data
            return item
        except KeyError:
            abort(404, message="Item not found.")
        
    def delete(self,id):
        try:
            del items[id]
            return {"message" : "Item deleted"}, 200
        except KeyError:
            abort(404, Message="Item doesnt found") 