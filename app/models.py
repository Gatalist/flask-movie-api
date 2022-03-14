from datetime import datetime
from app import db, login
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from settings import Config
import os
from werkzeug.utils import secure_filename
import uuid
from slugify import slugify


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    poster = db.Column(db.String())
    
    movies = db.relationship('Movie', backref='user', lazy='dynamic')

    def __repr__(self):
        return self.name

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def save_image(self, img):
        type_file = img.filename.split('.')[-1]
        img.filename = str(uuid.uuid4()) + '.' + type_file
        path = os.path.join(Config.STATIC_FOLDER, Config.FOLDER_MOVIE, secure_filename(img.filename))
        img.save(path)
        self.poster = path
        
    def get_image(self):
        return self.poster


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Genre(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    poster = db.Column(db.String())
    
    movies = db.relationship('Movie', backref='genre', lazy='dynamic')

    def __repr__(self):
        return self.name

    def save_image(self, img):
        type_file = img.filename.split('.')[-1]
        img.filename = str(uuid.uuid4()) + '.' + type_file
        path = os.path.join(Config.STATIC_FOLDER, Config.FOLDER_MOVIE, secure_filename(img.filename))
        img.save(path)
        self.poster = path

    def get_image(self):
        return self.poster


class Producer(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True, unique=True)
    poster = db.Column(db.String())
    
    movies = db.relationship('Movie', backref='producer', lazy='dynamic')

    def __repr__(self):
        return self.name

    def save_image(self, img):
        type_file = img.filename.split('.')[-1]
        img.filename = str(uuid.uuid4()) + '.' + type_file
        path = os.path.join(Config.STATIC_FOLDER, Config.FOLDER_MOVIE, secure_filename(img.filename))
        img.save(path)
        self.poster = path
    
    def get_image(self):
        return self.poster


# class Rating(UserMixin, db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     star = db.Column(db.Integer(), unique=True)
    
#     posts = db.relationship('Post', backref='author', lazy='dynamic')

#     def __repr__(self):
#         return self.star


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    slug = db.Column(db.String(150), index=True, unique=True)
    genres_id = db.Column(db.Integer, db.ForeignKey('genre.id'))
    release_date = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    producer_id = db.Column(db.Integer, db.ForeignKey('producer.id'))
    body = db.Column(db.Text(500))
    # rating = db.Column(db.String(100))
    poster = db.Column(db.String())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    publication = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    def __repr__(self):
        return self.title

    def save_image(self, img):
        type_file = img.filename.split('.')[-1]
        img.filename = str(uuid.uuid4()) + '.' + type_file
        path = os.path.join(Config.STATIC_FOLDER, Config.FOLDER_MOVIE, secure_filename(img.filename))
        img.save(path)
        self.poster = path

    def get_image(self):
        return self.poster

    def get_absolute_url(self):
        return f'/movie/{self.slug}'

    # def __setattr__(self, key, value):
    #     super(Movie, self).__setattr__(key, value)
    #     if key == 'title':
    #         self.slug = slugify(self.title)

    def __save__(self):
        self.slug = slugify(self.title)