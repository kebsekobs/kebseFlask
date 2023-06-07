from datetime import datetime
from hashlib import md5

from flask_login import UserMixin
from sqlalchemy import UniqueConstraint
from werkzeug.security import generate_password_hash, check_password_hash

from kebseApp import db

things_in_shops = db.Table('things in shops',
                           db.Column('shop_id', db.Integer, db.ForeignKey('shops.id')),
                           db.Column('thing_id', db.Integer, db.ForeignKey('things.id'))
                           )


class Shop(db.Model):
    __tablename__ = "shops"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    things = db.relationship("Thing", secondary=things_in_shops)


class Thing(db.Model):
    __tablename__ = "things"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20))
    price = db.Column(db.Integer)
    shop = db.relationship("Shop", secondary=things_in_shops)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.String(64), nullable=False, unique=True)
    username = db.Column(db.String(128), nullable=False, unique=True)
    token = db.Column(db.String(256), nullable=False, unique=True)
    last_seen = db.Column(db.DateTime(), nullable=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def avatar(self, size):
        # return 'https://www.gravatar.com/avatar/' + md5(self.mail.encode('utf-8')).hexdigest() + '?d=mm&s=' + str(size)
        return "../static/img/"+self.user_id+".jpg"

    def correct_data(self):
        if self.last_seen.strftime("%B %d, %Y at %H:%M") == datetime.now().strftime("%B %d, %Y at %H:%M"):
            return 'Online'
        elif self.last_seen.strftime("%B %d, %Y") == datetime.now().strftime("%B %d, %Y"):
            return self.last_seen.strftime("Was online: %H:%M")
        elif self.last_seen.strftime("%Y") == datetime.now().strftime("%Y"):
            return self.last_seen.strftime("Was online: %B %d at %H:%M")
        return self.last_seen.strftime("Was online: %B %d, %Y at %H:%M")
