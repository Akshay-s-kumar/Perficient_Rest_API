from db import db
from sqlalchemy import Text
class UserModel(db.Model):
    __tablename__ = "users"

    user_id = db.Column(db.Integer, primary_key=True)
    email_id = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(Text,nullable=False)

