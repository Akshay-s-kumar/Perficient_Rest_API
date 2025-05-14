from flask import Flask,request
from db import users,stores,items,tags
import uuid
app = Flask(__name__)

#endpoints for Users
@app.post("/register")
def create_user():
    response_data = request.get_json()
    user = {**response_data,"user_name":response_data["email_id"][:4]}
    users[user["user_name"]] = user
    return user, 201

@app.get("/user/<string:id>")
def get_user(id):
    if id in users:
        return users[id]
    else:
        return {"message":"User doesnt exist"}, 404

@app.delete("/delete/<string:id>")
def delete_user(id):
    if id in users:
        del users[id]
        return {"Message" : "User deleted"}, 200
    else:
        return {"Message":"User doesnt exist"}, 404

#endpoints for Stores
@app.post("/store")
def create_store():
    response_data = request.get_json()
    store_id = uuid.uuid4().hex
    store = {**response_data,"store_id":store_id}
    stores[store_id] = store
    return store, 201

@app.get("/store")
def get_stores():
    return stores, 200

@app.get("/store/<string:id>")
def get_store(id):
    if id in stores:
        return stores[id], 200
    else:
        return {"message" : "Store not found"}, 404
    
@app.delete("/store/<string:id>")
def del_store(id):
    if id in stores:
        del stores[id]
        return {"message" : "Store deleted"}, 200
    else:
        return {"Message" : "Store doesnt found "}, 404
       
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
    

#endpoints for items
@app.post("/item")
def create_item():
    response_data = request.get_json()
    item_id = len(items) + 1
    item = {**response_data,"item_id":item_id}
    stores[response_data["store_id"]]["items"].append(item)
    items[item_id] = item
    return item, 201

@app.get("/item")
def get_items():
    return items, 200

@app.get("/item/<string:id>")
def get_item(id):
    if id in items:
        return items[id], 200
    else:
        return {"message" : "Store not found"}, 404
    
@app.put("/item/<string:id>")
def update_item(id):
    response_data = request.get_json()
    if id in items:
        items[id] |= response_data
        return {"message": "Item updated successfully", "item": items[id]}, 200
    else:
        return {"error": "Item not found"}, 404
    
@app.delete("/item/<string:id>")
def del_item(id):
    if id in items:
        del items[id]
        return {"message" : "Item deleted"}, 200
    else:
        return {"Message" : "Item doesnt found "}, 404
       