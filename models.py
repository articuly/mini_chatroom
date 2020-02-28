from libs import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


# 用户数据库
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True,autoincrement=True)
    realname = db.Column(db.String)
    username = db.Column(db.String, unique=True)
    password = db.Column(db.String)
    sex = db.Column(db.Integer)
    city = db.Column(db.String)
    education = db.Column(db.String)
    hobby = db.Column(db.String)
    is_single = db.Column(db.Integer)
    message = db.relationship('Message')

    def hash_password(self, password):
        self.password = generate_password_hash(password)

    def validate_password(self, password):
        return check_password_hash(self.password, password)


# 消息数据库
class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    send_time = db.Column(db.DateTime, default=datetime.now)
    content = db.Column(db.String, nullable=True)
    from_user = db.Column(db.String, db.ForeignKey('user.username'))
    to_user = db.Column(db.String)
