from flask import Flask, jsonify
from flask_restful import Api
from flask_jwt import JWT

from security import authenticate, identity as identity_function
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'lance'
api = Api(app)

@app.before_first_request
def create_tables():
	db.create_all()

# change authentication URL (must happens before jwt = JWT(...))
#app.config['JWT_AUTH_ARL_RULE'] = '/login'
jwt = JWT(app, authenticate, identity_function)

# change token expiration time to 1 hour
#app.config['JWT_EXPIRATION_DELTA'] = timedelta(seconds=3600)

# change authentication key name to 'email' instead of 'username'
#app.config['JWT_AUTH_USERNAME_KEY'] = 'email'

# change authentication response handler
@jwt.auth_response_handler
def customized_response_handler(access_token, identity):
    return jsonify({
                        'access_token': access_token.decode('utf-8'),
                        'user_id': identity.id
                   })

# jwt error handler
@jwt.jwt_error_handler
def customized_error_handler(error):
    return jsonify({
                       'message': error.description,
                       'code': error.status_code
                   }), error.status_code

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')
api.add_resource(StoreList, '/stores')
api.add_resource(Store, '/store/<string:name>')
api.add_resource(UserRegister, '/register')

if __name__ == '__main__':
	from db import db
	db.init_app(app)
	app.run(port=5000, debug=True)






