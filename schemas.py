from marshmallow import Schema,fields

class UserSchema(Schema):
    email_id = fields.Str(required=True)
    password = fields.Str(required=True)
    user_name = fields.Str(dump_only=True)

class UserUpdateSchema(Schema):
    email_id = fields.Str()
    password = fields.Str()
    user_name = fields.Str()

class StoreSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    store_id = fields.Str(dump_only=True)
 
class ItemSchema(Schema):
    id = fields.Str(dump_only=True)
    name = fields.Str(required=True)
    price = fields.Float(required=True)   
    store_id = fields.Str(required=True) 
    
class ItemUpdateSchema(Schema):
    name = fields.Str()
    price = fields.Float()

