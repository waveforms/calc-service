from typing import List, Dict
from flask import Flask, render_template, flash, redirect, url_for, request
import mysql.connector
import json
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from components.forms import LoginForm, RegistrationForm, PostForm
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
#from flask_login import LoginManager
from flask_login import UserMixin
import flask_login
from flask_login import login_user, logout_user, current_user
from flask_api import FlaskAPI, status, exceptions
from flask_bootstrap import Bootstrap
from flask_cors import CORS
import os
from flask_restful import Resource, Api
from . import maxsum


#e = create_engine('sqlite:///test.db')

#app = Flask(__name__)
app = FlaskAPI(__name__)
CORS(app)
Bootstrap(app)
app.config.from_object(Config)
api = Api(app)
# app.config['STATIC_FOLDER'] = 'static'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(id):
    try:
        value = int(id)
    except ValueError:
        return redirect(url_for('login'))
    return User.query.get(int(value))

# Our mock database.
#users = {'foo@bar.tld': {'password': 'secret'}}


# @login_manager.user_loader
# def user_loader(email):
#     if email not in users:
#         return

#     user = User()
#     user.id = email
    return user

# @login_manager.request_loader
# def request_loader(request):
#     # email = request.form.get('email')
#     # if email not in users:
#     #     return

#     user = User()
#     user.id = email

#     # DO NOT ever store passwords in plaintext and always compare password
#     # hashes using constant-time comparison!
#     user.is_authenticated = request.form['password'] == users[email]['password']

#     return user


# login = LoginManager(app)
# login.login_view = 'login'

# login_manager.init_app(app)

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if request.method == 'GET':
#         return '''
#                <form action='login' method='POST'>
#                 <input type='text' name='email' id='email' placeholder='email'/>
#                 <input type='password' name='password' id='password' placeholder='password'/>
#                 <input type='submit' name='submit'/>
#                </form>
#                '''

#     email = request.form['email']
#     if request.form['password'] == users[email]['password']:
#         user = User()
#         user.id = email
#         flask_login.login_user(user)
#         return redirect(url_for('protected'))

#     return 'Bad login'


@app.route('/logout')
def logout():
    flask_login.logout_user()
    flash('Please Login or register.')
    return redirect(url_for('login'))

@login_manager.unauthorized_handler
def unauthorized_handler():
    flash('Please Login or register.')
    return redirect(url_for('login'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/protected')
@flask_login.login_required
def protected():
    return 'Logged in as: ' + flask_login.current_user.id


@app.route('/')
@app.route('/index', methods=['GET', 'POST'])
@flask_login.login_required
def index():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post is now live!')
        return redirect(url_for('index'))
    # page = request.args.get('page', 1, type=int)
    posts = current_user.followed_posts()
    return render_template('index.html', title='Home', form=form,
                           posts=posts)
    
    # user = {'username': 'Miguel'}
    # posts = [
    #     {
    #         'author': {'username': 'John'},
    #         'body': 'Beautiful day in Portland!'
    #     },
    #     {
    #         'author': {'username': 'Susan'},
    #         'body': 'The Avengers movie was so cool!'
    #     }
    # ]
    # return render_template('index.html', title='Home', posts=posts)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def followed_posts(self):
        return self.posts

    def __repr__(self):
        return '<User {}>'.format(self.username)

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)
 


class Calculation_Assets(Resource):
    def post(self):
        json_data = request.get_json(force=True)
        print(json.dumps(json_data))
        sum_lp = maxsum.convert_json(json_data)
        print(sum_lp)
        e = db.get_engine()
        conn = e.connect()
        return {'data': {'sum_lp' : sum_lp}}
        # query = conn.execute("select * from annotation where frame_id=?",(frame_id))
        # result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        # return result

api.add_resource(Calculation_Assets, '/API/v1/calc_assets')  # bind url identifier to class; also make it querable

# notes = {
#     0: 'do the shopping',
#     1: 'build the codez',
#     2: 'paint the door',
# }

# def note_repr(key):
#     return {
#         'url': request.host_url.rstrip('/') + url_for('notes_detail', key=key),
#         'text': notes[key]
#     }


# @app.route("/notes_list", methods=['GET', 'POST'])
# def notes_list():
#     """
#     List or create notes.
#     """
#     if request.method == 'POST':
#         note = str(request.data.get('text', ''))
#         idx = max(notes.keys()) + 1
#         notes[idx] = note
#         return note_repr(idx), status.HTTP_201_CREATED

#     # request.method == 'GET'
#     return [note_repr(idx) for idx in sorted(notes.keys())]


# @app.route("/API/v1/<int:key>/", methods=['GET', 'PUT', 'POST', 'DELETE'])
# def notes_detail(key):
#     """
#     Retrieve, update or delete note instances.
#     """
#     if request.method == 'POST':
#         note = str(request.data.get('json_text', ''))
#         notes[key] = note
#         return note_repr(key)

#     elif request.method == 'DELETE':
#         notes.pop(key, None)
#         return '', status.HTTP_204_NO_CONTENT

#     # request.method == 'GET'
#     if key not in notes:
#         raise exceptions.NotFound()
#     return note_repr(key)


@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

if __name__ == '__main__':
    app.run(host='0.0.0.0')