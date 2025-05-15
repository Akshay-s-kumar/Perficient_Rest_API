from flask_smorest import abort, Blueprint 
from flask.views import MethodView
from schemas import UserSchema, UserUpdateSchema
from db import users

blp = Blueprint("users",__name__,description= "Operations on Users")

@blp.route("/user")
class Users(MethodView):

    @blp.arguments(UserSchema)
    @blp.response(201,UserSchema)
    def post(self,user_data):
        try:
            user = {**user_data,"user_name":user_data["email_id"][:4]}
            user_name = user["user_name"]
            users[user_name] = user
            return user
        except KeyError:
            abort(400,message="User not created")
    
    @blp.response(200,UserSchema(many=True))
    def get(self):
        try:
            return users.values()
        except KeyError:
            abort(404,message="User not found")

@blp.route("/user/<string:name>")
class User(MethodView):

    @blp.response(200,UserSchema)
    def get(self,name):
        try:
            return users[name]
        except KeyError:
            abort(400, message="User doesnt exist")

    @blp.arguments(UserUpdateSchema)
    @blp.response(200, UserSchema)
    def put(self,user_data,name):
        try:
            users[name] |= user_data
            return users[name]
        except KeyError:
            abort(404, message="User not found")

    def delete(self,name):
        try:
            del users[name]
            return {"Message" : "User deleted"}
        except KeyError:
            abort(400, message="User doesnt exist")
        

"""
#endpoints for tags
@app.post("/store/<string:id>/tag")
def create_tag(id):
    response_data = request.get_json()
    tag_id = len(tags) + 1
    tag = {**response_data,"tag_id":tag_id}
    tags[response_data["name"]] = []
    stores[id]["tags"].append(tag)
    return tags, 201

@app.get("/item/<string:item_id>/tag/<string:tag_name>")
def link_item_tag(item_id, tag_name):
    # Check if the tag exists
    if tag_name not in tags:
        return {"message": "Tag not found"}, 404
    
    # Check if the item exists
    for item in stores.get("items", []):
        if item["item_id"] == item_id:
            # Link the item to the tag
            tags[tag_name].append(item)
            return {tag_name: tags[tag_name]}, 200
    
    # If no matching item was found
    return {"message": "Item not found"}, 404


@app.get("/store/<string:id>/tag")
def get_tag(id):
    if id in stores:
        return stores[id]["tags"], 200
    else:
        return {"message" : "Error"}, 404
    
"""

