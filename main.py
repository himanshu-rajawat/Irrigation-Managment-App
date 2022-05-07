from flask import Flask, jsonify, request, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_restful import Resource, Api, reqparse, fields, marshal_with
from flask_cors import CORS, cross_origin
from functools import wraps
import jwt

app = Flask(__name__)
bcrypt = Bcrypt(app)
CORS(app)
db = SQLAlchemy(app)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = 'SECRET_KEY'



class User(db.Model):
    __tablename__ = 'user'
    user_id = db.Column(db.Integer, primary_key=True)
    contact_number = db.Column(db.String(10), unique=True)
    username = db.Column(db.String(255), unique=True, nullable=True)
    password = db.Column(db.String(255), nullable=False)
    lastlogin = db.Column(db.String(255))
    datas = db.relationship('Data',backref='User',passive_deletes=True)

class Crop(db.Model):
    __tablename__ = 'crop'
    crop_id = db.Column(db.Integer, autoincrement  = True, primary_key = True)
    crop_name = db.Column(db.String(20), nullable = False, unique = True)
    ideal_lower = db.Column(db.Integer,nullable = False)
    ideal_higher = db.Column(db.Integer,nullable = False)
    datas = db.relationship('Data',backref='Crop',passive_deletes=True)

class Data(db.Model):
    __tablename__ = 'data'
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id',ondelete='CASCADE'),primary_key = True)
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.crop_id',ondelete='CASCADE'),primary_key = True)
    moisture_content = db.Column(db.Integer,nullable = False)



def token_required(f):
    @wraps(f)
    def decorated(*args,**kwargs):
        token = None
        data = None
        # data = request.get_json()
        auth_headers = request.headers.get('Authorization', '').split()

        invalid_msg = {
            'message': 'Invalid token. Registeration and / or authentication required',
            'authenticated': False
        }
        expired_msg = {
            'message': 'Expired token. Reauthentication required.',
            'authenticated': False
        }

        if len(auth_headers) != 2:
            return jsonify(invalid_msg), 401

        try:
            token = auth_headers[1]

        # if not token:
        except:
            return jsonify({'message':'Token is missing'})

        try:
            data = jwt.decode(token,app.config['SECRET_KEY'],algorithms="HS256")
            current_user = User.query.filter_by(contact_number = data['user']).first()
            current_user.lastlogin = datetime.today().strftime("%d/%m/%Y, %H:%M:%S")
            db.session.commit()
            id = current_user.id
        except:
            res = jsonify({'message':'token is invalid'})
            return make_response((res),401)
        return f(current_user,*args,**kwargs)
    return decorated

user_registration_args = reqparse.RequestParser()
user_registration_args.add_argument("contact_number")
user_registration_args.add_argument("username")
user_registration_args.add_argument("password")

user_login_args = reqparse.RequestParser()
user_login_args.add_argument("contact_number")
user_login_args.add_argument("password")

create_crop_args = reqparse.RequestParser()
create_crop_args.add_argument("crop_name")

delete_crop_args = reqparse.RequestParser()
delete_crop_args.add_argument("crop_name")

class UserRegistrationAPI(Resource):
    def post(self):
        args = user_registration_args.parse_args()
        contact_number = args.get("contact_number",None)
        username = args.get("username",None)
        password = args.get("password",None)
        if contact_number == None or username ==  None or password == None:
             return None
        else:
            try:
                hashed_password = bcrypt.generate_password_hash(password)
                user_new = User(contact_number = contact_number,password=hashed_password,username=username)
                db.session.add(user_new)
                db.session.commit()
                return make_response(jsonify({"contact_number": contact_number, "username": username}),200)
            except:
                res = jsonify({"message":"username and phone number should be unique"})
                return make_response(res,500)

class UserLoginAPI(Resource):
    def post(self):
        args = user_login_args.parse_args()
        contact_number = args.get("contact_number",None)
        password = args.get("password",None)
        user = User.query.filter_by(contact_number=contact_number).first()
        if user != None:
            if bcrypt.check_password_hash(user.password, password) and user.id != -1:
                login_user(user)
                token = jwt.encode({'user':current_user.contact_number,'exp': datetime.utcnow()+ timedelta(minutes=30)},app.config['SECRET_KEY'],algorithm="HS256")
                print(token)
                return jsonify({'token': token})
                response = jsonify({"username":current_user.username})
                return response
            else:
                return make_response('could not verify',401,{'WWW-Authenticate':'Basic realm="Login Required"'})
        else:
            return make_response(jsonify({"message":"user does not exist"}),401)

class UserDashboardAPI(Resource):
    @token_required
    def get(current_user,self):
        data_objects = Data.query.filter_by(user_id=current_user.user_id).all()
        response = {}
        username = current_user.username
        response['username'] = username
        for object in data_objects:
            current_moisture = object.moisture_content
            crop_name = object.crop_id.crop_name
            ideal_lower = object.crop_id.ideal_lower
            ideal_higher = object.crop_id.ideal_higher
            response[crop_name] = {'current_moisture':current_moisture,'ideal_lower':ideal_lower,'ideal_higher':ideal_higher}
        return jsonify(response)

class CreateCropAPI(Resource):
    @token_required
    def post(current_user,self):
        args = create_crop_args.parse_args()
        crop_name = args.get("crop_name",None)
        crop_id = Crop.query.filter_by(crop_name=crop_name).first().crop_id
        try:
            new_data_object = Data(user_id = current_user.id,crop_id = crop_id)
            db.session.add(new_data_object)
            db.session.commit()
            return make_response(jsonify({"crop_name": crop_name, "username": current_user.name}),200)
        except:
            res = jsonify({"message":"this crop already exists"})
            return make_response(res,500)

class DeleteCropAPI(Resource):
    @token_required
    def delete(current_user,self):
        args = delete_crop_args.parse_args()
        crop_name = args.get("crop_name",None)
        crop_id = Crop.query.filter_by(crop_name=crop_name).first().crop_id
        data_object = Data.query.filter_by(crop_id = crop_id).first()
        db.session.delete(data_object)
        sb.session.commit()
        return make_response(jsonify({"crop_name": crop_name, "username": current_user.name}),200)

api.add_resource(UserRegistrationAPI,"/signupapi")
api.add_resource(UserLoginAPI,"/loginapi")
api.add_resource(UserDashboardAPI,"/dashboardapi")
api.add_resource(CreateCropAPI,"/createcropapi")
api.add_resource(DeleteCropAPI,"/deletecropapi")

if __name__ == '__main__':
    app.run(debug = True)
