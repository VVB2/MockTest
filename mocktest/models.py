from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from datetime import datetime
from mocktest import db, login_manager, app
from flask_login import UserMixin

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
    hackos = db.Column(db.Integer, default=20)
    phoneno = db.Column(db.String(20), default='None')
    address = db.Column(db.String(255), default='None')
    gender = db.Column(db.String(6), nullable=False)
    badge = db.Column(db.String(20), default='Novice')
    created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

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

