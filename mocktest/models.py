import json
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import date,datetime
from mocktest import db, login_manager, app
from flask_login import UserMixin
from sqlalchemy_serializer import SerializerMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password = db.Column(db.String(60), nullable=False)
    phoneno = db.Column(db.String(20), default='None')
    address = db.Column(db.String(255), default='None')
    gender = db.Column(db.String(6), nullable=False)
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    Marksobtained = db.relationship('Marks', backref='author', lazy=True)

    def get_reset_token(self, expires_sec = 600):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)
    
    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"

class Java(db.Model, UserMixin):
    __tablename__ = 'JAVA'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer)
    subject = db.Column(db.String(10), nullable=False)
    module = db.Column(db.String(30), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(5), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    optiona = db.Column(db.String(100))
    optionb = db.Column(db.String(100))
    optionc = db.Column(db.String(100))
    optiond = db.Column(db.String(100))

    def __repr__(self):
        return f"Variable('{self.module}', '{self.question}')"

class Python(db.Model, UserMixin):
    __tablename__ = 'PYTHON'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    question_id = db.Column(db.Integer)
    subject = db.Column(db.String(10), nullable=False)
    module = db.Column(db.String(30), nullable=False)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(5), nullable=False)
    reason = db.Column(db.String(255), nullable=False)
    optiona = db.Column(db.String(100))
    optionb = db.Column(db.String(100))
    optionc = db.Column(db.String(100))
    optiond = db.Column(db.String(100))

    def __repr__(self):
        return f"Variable('{self.module}', '{self.question}')"

class Marks(db.Model, UserMixin, SerializerMixin):
    __tablename__ = 'MARKS'

    serialize_rules = ('-user_id','-id')

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    subject = db.Column(db.String(10), nullable=False)
    module = db.Column(db.String(30), nullable=False)
    marks_obtained = db.Column(db.Integer, nullable=False)
    attempted_on = db.Column(db.DateTime, nullable=False, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __repr__(self):
        return f"Variable('{self.id}', '{self.module}')"



