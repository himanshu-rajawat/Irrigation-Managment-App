
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
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id',ondelete='CASCADE'))
    crop_id = db.Column(db.Integer, db.ForeignKey('crop.crop_id',ondelete='CASCADE'))
    moisture_content = db.Column(db.Integer,nullable = False)
