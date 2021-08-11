from flask.json import jsonify
from flask_restful import Resource, reqparse, inputs
from flask_login import login_user, login_required, current_user, logout_user
from flask_restful_swagger import swagger
from flask_bcrypt import Bcrypt
from flask.json import jsonify
from flask.views import MethodView
from app.models.user import UserModel, UserLoginRequest, UserRegisterRequest
from app.models.country import CountryModel
from app.models.state import StateModel
from app.schemas.user import UserSchema, user_schema, users_schema_minimal, user_schema_minimal
from app.schemas.country import countries_schema_minimal
from app.schemas.state import states_schema_minimal
from datetime import datetime


_user_login_parser = reqparse.RequestParser()
_user_login_parser.add_argument(
    "email",
    type=inputs.regex('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$'),
    required=True,
    help="Invalid email address"
)
_user_login_parser.add_argument(
    "password",
    type=str,
    required=True,
    help="This field cannot be blank"
)


class UserLogin(MethodView):


    @swagger.operation(
        notes='Login User',
        parameters=[
            {
              "name": "body",
              "description": "User login credentials",
              "required": True,
              "allowMultiple": False,
              "dataType": UserLoginRequest.__name__,
              "paramType": "body"
            }
        ],
        responseClass=UserModel.__name__,
        responseMessages=[
            {
              "code": 200,
              "message": "Successful login. Returns user record"
            },
            {
              "code": 400,
              "message": "Invalid credentials!"
            }
        ]
    )
    def post(self):
        data = _user_login_parser.parse_args()

        user = UserModel.find_user_by_email(data["email"])
        bcrypt = Bcrypt()

        if user and bcrypt.check_password_hash(user.password, data["password"]):
            login_user(user)
            return user_schema.dump(user), 200

        return {
            "message": "Invalid credentials!"
        }, 400



_user_parser = _user_login_parser.copy()
_user_parser.add_argument(
    "first_name",
    type=str,
    required=True
)

_user_parser.add_argument(
    "last_name",
    type=str,
    required=True
)

_user_parser.add_argument(
    "phone",
    type=str,
    required=False
)

_user_parser.add_argument(
    "mobile",
    type=str,
    required=False
)

_user_parser.add_argument(
    "city",
    type=str,
    required=False
)

_user_parser.add_argument(
    "zip",
    type=str,
    required=False,
)

_user_parser.add_argument(
    "country",
    type=int,
    required=False
)

_user_parser.add_argument(
    "state",
    type=int,
    required=False
)

_user_update_parser = _user_parser.copy()
_user_update_parser.remove_argument('password')
_user_update_parser.add_argument(
    "password",
    type=str,
    required=False,
)

class UserList(Resource):
    @swagger.operation(
        notes='List Users',
        responseClass="string",
        parameters=[],
        responseMessages=[
            {
              "code": 200,
              "message": "Users List"
            }
        ]
    )
    def get(self):
        users = UserModel.find_all()
        return jsonify({ "users": users_schema_minimal.dump(users)})


class ListUserById(MethodView):

    @swagger.operation(
        notes='Get Users By Id',
        responseClass=UserModel.__name__
    )

    def get(self, _id):
        user = UserModel.find_by_id(_id)
        print(user)
        if user:
            return addPageMetaData(user)
        return {'message': 'User not found'}, 404


    @swagger.operation(notes="delete user by ID",
    parameters=[
            {
                "name": "_id",
                "description": "The Id of the user",
                "required": True,
                "allowMultiple": False,
                "dataType": "string",
                "paramType": "path",
            }
        ])
    # @login_required
    def delete(self, _id):
        user = UserModel.find_by_id(_id)
        user.remove_from_db()

        if user:
            return {
                "message": "User id {} Deactivated!".format(_id)
            }, 200
        return {
            "message": "User not found!"
        }, 404


    @swagger.operation(notes="Update an User by id",
        parameters=[
            {
                "name": "user",
                "description": "The Id of the User",
                "required": True,
                "allowMultiple": False,
                "dataType": UserRegisterRequest.__name__,
                "paramType": "body",
            }
        ])
    @login_required
    def put(self, _id):
            
        data = _user_update_parser.parse_args()

        country_record = None
        if (data['country']):
            #check if country ud exists
            country_record = CountryModel.find_by_id(data['country'])
            if country_record is None:
                return {'message': 'Country id not found'}, 404

        state_record = None
        if (data['state']):
            #check if state ud exists
            state_record = StateModel.find_by_id(data['state'])
            if state_record is None:
                return {'message': 'State id not found'}, 404


        user = UserModel.find_by_id(_id)

        if user:
            user.update_details(first_name = data['first_name'],
                               last_name = data['last_name'],
                               phone =  data['phone'],
                               mobile = data['mobile'],
                               city =  data['city'],
                               zip =  data['zip'],
                               country = country_record,
                               updated_at = datetime.utcnow(),
                               state = state_record)

            if (data.get('password')):
                user.update_password(data['password'])

            return addPageMetaData(user)

        return {'message': 'User not found'}, 404


class UserLogout(Resource):
    @swagger.operation(
        notes='Logout User',
        responseClass="string",
        parameters=[],
        responseMessages=[
            {
              "code": 200,
              "message": "Successful logout"
            }
        ]
    )
    def get(self):
        logout_user()
        return {
            "message": "User Logged Out"
        }, 200

class MyProfile(Resource):
    @swagger.operation(
    notes='Gets logged user from user sesssion',
    nickname='get',
    responseClass=UserModel.__name__,
    parameters=[ ],
    responseMessages=[
        {
            "code": 200,
            "message": "User found. The user model is return in the response body"
        },
        {
            "code": 404,
            "message": "User not logged in"
        }
    ]
    )
    @login_required
    def get(self):
        user = UserModel.find_by_id(current_user.get_id())
        if user:
            return user_schema.dump(user)

        return {
            "message": "User not found!"
        }, 404


def addPageMetaData(user):
    countries = CountryModel.find_all('position')
    states = StateModel.find_all('position')

    return jsonify({"user" : user_schema.dump(user),
                    "countries" : countries_schema_minimal.dump(countries),
                    "states": states_schema_minimal.dump(states)
                    })


class CreateUser(MethodView):
    
    @swagger.operation(
        notes='Get User Meta Data',
        responseClass=UserModel.__name__,
        responseMessages=[
            {
              "code": 200,
              "message": "Return user meta data"
            }
        ]
    )
    def get(self):
        
        user = UserModel({})
        return addPageMetaData(user)

    
    @swagger.operation(
        notes='Register User',
        responseClass=UserModel.__name__,
        parameters=[
            {
                "name": "user",
                "description": "User data",
                "required": True,
                "allowMultiple": False,
                "dataType": UserRegisterRequest.__name__,
                "paramType": "body"
            }
        ],
        responseMessages=[
            {
              "code": 200,
              "message": "Return the created user record"
            },
            {
              "code": 400,
              "message": "User exists!"
            }
        ]
    )
    def post(self):

        data = _user_parser.parse_args()

        if UserModel.find_user_by_email(data["email"]):
            return {
                "message": "User exists!"
            }, 400

        country = None
        if (data['country']):
            #check if country ud exists
            country = CountryModel.find_by_id(data['country'])
            if country is None:
                return {'message': 'Country id not found'}, 404

        state = None
        if (data['state']):
            #check if state ud exists
            state = StateModel.find_by_id(data['state'])
            if state is None:
                return {'message': 'State id not found'}, 404
        
        user = UserModel(data)
        user.country = country
        user.state = state
        user.save_to_db()
        return addPageMetaData(user)
