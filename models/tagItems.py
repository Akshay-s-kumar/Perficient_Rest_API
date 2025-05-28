from db import db

class TagItemsModel(db.Model):

    __tablename__ = "tagitems"

    id = db.Column(db.Integer,primary_key = True)
    tag_id = db.Column(db.Integer,db.ForeignKey("tags.id"))
    item_id = db.Column(db.Integer,db.ForeignKey("items.id"))