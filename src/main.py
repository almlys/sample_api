#!/usr/bin/env python

"""
Sample Flask application with SQLAlchemy
"""

import argparse

from flask import Flask, request, render_template, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask.ext.cache import Cache

# Setup application configuration, database, and type of cache
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://api:!456@db:3306/api_db?charset=utf8'
db = SQLAlchemy(app)
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

def is_debug():
    return False

# Entities
class User(db.Model):
    """
    Represents our User entity
    """
    id = db.Column(db.String(250), primary_key=True)
    password = db.Column(db.String(100))
    phone = db.Column(db.String(15))

    def __init__(self, id, password=None, phone=None):
        self.id = id
        self.password = password
        self.phone = phone

    def __repr__(self):
        return '<User %s>' % (self.id,)

# API End-points
@app.route('/')
@cache.cached(timeout=120, unless=is_debug)
def index():
    """
    Render simple static html, with some code to play with the api.
    """
    return render_template('index.html')


@app.route('/user/<id>', methods=['GET'])
@cache.memoize(timeout=120, unless=is_debug)
def get_user(id):
    """
    Returns a user as json by its id
    :param id: 
    :return: 
    """
    user = User.query.filter_by(id=id).first()
    if user is None:
        return make_response(sucess=False, reason="Cannot find user")

    return make_response(sucess=True, user={'username': user.id, 'password': user.password, 'phone': user.phone})


@app.route('/user', methods=['POST'])
def create_user():
    """
    Create new user within the DB
    :return: 
    """
    id = request.form.get('id')
    password = request.form.get('password')
    phone = request.form.get('phone')

    if id is None or len(id) == 0:
        return make_response(sucess=False, reason="Id is empty!")
    if password is None or len(password) == 0:
        return make_response(sucess=False, reason="Password is empty!")
    if phone is None or len(phone) == 0:
        return make_response(sucess=False, reason="Phone is empty!")

    try:
        db.session.add(User(id, password, phone))
        db.session.commit()
        cache.delete_memoized(get_user, id)
        return make_response(sucess=True)
    except Exception:
        import traceback
        print(traceback.format_exc())
        return make_response(sucess=False, reason="DB Error (maybe user already exists)")


def make_response(sucess=True, reason='', user=None):
    return jsonify({'success': sucess, 'reason': reason, 'user': user})


@app.route('/user/<id>', methods=['DELETE'])
def delete_user(id):
    """
    Delete requested user by id from the DB
    :param id: 
    :return: 
    """
    user = User.query.filter_by(id=id).first()
    if user is None:
        return make_response(sucess=False, reason="Cannot find user to delete")
    try:
        db.session.delete(user)
        db.session.commit()
        # Delete it from the cache
        cache.delete_memoized(get_user, id)
        return make_response(sucess=True)
    except Exception:
        import traceback
        print(traceback.format_exc())
        return make_response(sucess=False, reason="DB Error (cannot delete user)")


if __name__ == '__main__':
    """
    Main code, with some operations to create or delete databases.
    """
    parser = argparse.ArgumentParser(description='API Test Service Server')
    parser.add_argument('--drop-database',
                        action="store_true", dest="dropDatabase",
                        help=("Drops database"), default=False)
    parser.add_argument('--init-database',
                        action="store_true", dest="initDatabase",
                        help=("Inits database"), default=False)

    args = parser.parse_args()

    if args.dropDatabase:
        db.drop_all()
    if args.initDatabase:
        db.create_all()
    db.session.commit()
