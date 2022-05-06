from flask import Flask, jsonify, request, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
# from flask_restful import Resource, Api, reqparse, fields, marshal_with
# from flask_cors import CORS, cross_origin
# from functools import wraps
# import jwt

app = Flask(__name__)
bcrypt = Bcrypt(app)
# CORS(app)
db = SQLAlchemy(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.sqlite3'
app.config['SECRET_KEY'] = 'SECRET_KEY'

# hashed_password = bcrypt.generate_password_hash(form.password.data)
# bcrypt.check_password_hash(user.password, form.password.data)


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

db.create_all()
db.session.commit()

# def token_required(f):
#     @wraps(f)
#     def decorated(*args,**kwargs):
#         token = None
#         data = None
#         # data = request.get_json()
#         auth_headers = request.headers.get('Authorization', '').split()
#
#         invalid_msg = {
#             'message': 'Invalid token. Registeration and / or authentication required',
#             'authenticated': False
#         }
#         expired_msg = {
#             'message': 'Expired token. Reauthentication required.',
#             'authenticated': False
#         }
#
#         if len(auth_headers) != 2:
#             return jsonify(invalid_msg), 401
#
#         try:
#             token = auth_headers[1]
#             print(token)
#
#         # print(request.get_json('x-access-token'))
#         # if data:
#         #     token = data['x-access-token']
#         #     print("got the token")
#
#         # if not token:
#         except:
#             return jsonify({'message':'Token is missing'})
#
#         try:
#             data = jwt.decode(token,app.config['SECRET_KEY'],algorithms="HS256")
#             current_user = User.query.filter_by(email = data['user']).first()
#             current_user.lastlogin = datetime.today().strftime("%d/%m/%Y, %H:%M:%S")
#             db.session.commit()
#             id = current_user.id
#         except:
#             res = jsonify({'message':'token is invalid'})
#             return make_response((res),401)
#         return f(current_user,*args,**kwargs)
#     return decorated
