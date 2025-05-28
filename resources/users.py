
from flask_smorest import abort, Blueprint 
from sqlalchemy.exc import SQLAlchemyError
from flask.views import MethodView
from schemas import UserSchema
from db import db
from models import UserModel
from flask_jwt_extended import create_access_token,jwt_required,get_jwt
from passlib.hash import pbkdf2_sha256
from blocklist import Blocklist


blp = Blueprint("users",__name__,description= "Operations on Users")

@blp.route("/register")
class UserRegister(MethodView):

    @blp.arguments(UserSchema)
    def post(self,user_data):
        if UserModel.query.filter(UserModel.email_id == user_data["email_id"]).first():
            abort(409,message="User with this email id alerady exists")
        user = UserModel(email_id=user_data["email_id"],password=pbkdf2_sha256.hash(user_data["password"]),)
        try:
            db.session.add(user)
            db.session.commit()
        except SQLAlchemyError:
            abort(400,message= "Request Failed")
        return {"message": "User created successfully"}, 201
@blp.route("/user")
class UserRegister(MethodView):

    @blp.response(200, UserSchema(many=True))
    def get(self):
        user = UserModel.query.all()
        return user
    
@blp.route("/user/<int:user_id>")
class UserRegister(MethodView):

    @blp.response(200, UserSchema)
    def get(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        return user

    def delete(self, user_id):
        user = UserModel.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
        return {"message": "User deleted."}, 200
    
@blp.route("/login")
class UserLogin(MethodView):

    @blp.arguments(UserSchema)
    def post(self,user_data):
        user = UserModel.query.filter(
            UserModel.email_id == user_data["email_id"]
        ).first()
        if user and pbkdf2_sha256.verify(user_data["password"],user.password):
            access_token = create_access_token(identity=str(user))
            return {"access_token":access_token},201
        abort(401, message="Invalid credentials.")

@blp.route("/logout")
class UserLogout(MethodView):

    @jwt_required()
    def post(self):
        jti = get_jwt()["jti"]
        Blocklist.add(jti)
        return {"Message":"Token revoked successfully"},200