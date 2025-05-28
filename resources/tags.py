from sqlalchemy.exc import SQLAlchemyError,IntegrityError
from flask_smorest import abort,Blueprint
from flask.views import MethodView
from schemas import TagSchema, TagItemSchema
from models import StoreModel,TagModel, TagItemsModel, ItemModel
from flask import jsonify
from db import db

blp = Blueprint("Tags",__name__,description="operations on Tags")

@blp.route("/store/<string:id>/tag/<string:tag_id>")
class TagItem(MethodView):
    @blp.response(200, TagSchema(many=True))
    def get(self, id, tag_id):
        store = StoreModel.query.get_or_404(id)
        tag = next((tag for tag in store.tags if str(tag.id) == tag_id), None)
        if not tag:
            abort(404, message="Tag not found in this store")
        return tag.items

@blp.route("/store/<string:id>/tag")
class TagItem(MethodView):

    @blp.response(200,TagSchema(many=True))
    def get(self,id):
        store = StoreModel.query.get_or_404(id)
        return store.tags.all()

    @blp.arguments(TagSchema)
    @blp.response(200,TagSchema)
    def post(self,tag_data,id):
        if not StoreModel.query.filter_by(id=id).first():
            abort(404, message="Store not found")
        if TagModel.query.filter(TagModel.store_id == id,tag_data["name"] == TagModel.name).first():
            abort(400, message="A tag with that name already exists in that store.")
        tag = TagModel(**tag_data,store_id = id)
        try:
            db.session.add(tag)
            db.session.commit()
        except IntegrityError:
            abort(500)
        return tag
    
@blp.route("/item/<string:item_id>/tag/<string:tag_id>")
class LinkTagsItems(MethodView):

    @blp.response(201,TagSchema)
    def post(self,item_id,tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        if item.store.id != tag.store.id:
            abort(400)
        item.tags.append(tag)
        try:
            db.session.add(item)
            db.session.commit()
        except SQLAlchemyError:
            abort(500,message="An error occurred while inserting the tag.")
        return tag

    @blp.response(200, TagItemSchema)
    def delete(self, item_id, tag_id):
        item = ItemModel.query.get_or_404(item_id)
        tag = TagModel.query.get_or_404(tag_id)
        if tag not in item.tags:
            abort(404, message="Item is not associated with this tag.")
        stmt = TagItemsModel.__table__.delete().where(
            TagItemsModel.item_id == item_id,
            TagItemsModel.tag_id == tag_id
        )
        try:
            db.session.execute(stmt)
            db.session.commit()
        except SQLAlchemyError:
            abort(500, message="An error occurred while removing the tag.")
        return {"message": "Item removed from tag", "item": item, "tag": tag}

@blp.route("/tag/<string:id>")
class Tag(MethodView):

    @blp.response(200, TagSchema)
    def get(self,id):
        tag = TagModel.query.get_or_404(id)
        return tag
    
    def delete(self, id):
        tag = TagModel.query.get_or_404(id)
        if not tag.items:
            db.session.delete(tag)
            db.session.commit()
            return {"message": "Tag deleted."}
        abort(400,message="Could not delete tag. Make sure tag is not linked with any items",)