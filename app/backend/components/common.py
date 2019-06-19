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
#from flask_api import FlaskAPI, status, exceptions
from flask_bootstrap import Bootstrap
from flask_cors import CORS
import os
from flask_restful import Resource, Api
from . import maxsum
from sqlalchemy import desc



app = Flask(__name__)
CORS(app, supports_credentials=True)
Bootstrap(app)
app.config.from_object(Config)
api = Api(app)
# app.config['STATIC_FOLDER'] = 'static'
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

@login_manager.user_loader
def load_user(id):
    try:
        value = int(id)
    except ValueError:
        return redirect(url_for('login'))
    return User.query.get(int(value))


    return user


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


# @app.route('/protected')
# @flask_login.login_required
# def protected():
#     return 'Logged in as: ' + flask_login.current_user.id


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
    def get(self, id):
        post = Post.query.filter_by(user_id=id).order_by(desc('timestamp')).first()
        if (post):
            print(post.body)
            return {'data': json.loads(post.body)}
        else:
            return {'data': None }
         
    def post(self, id):
        json_data = request.get_json(force=True)
        #Post(body=form.post.data, author=current_user)
        post = Post(user_id=id, body=json.dumps(json_data))
        db.session.add(post)
        db.session.commit()
        flash('Your json tree was saved.')
        print(json.dumps(json_data))
        #+ flask_login.current_user.id
        sum_lp = maxsum.convert_json(json_data)
        print(sum_lp)
        e = db.get_engine()
        conn = e.connect()
        return {'data': {'sum_lp' : sum_lp}}
        # query = conn.execute("select * from annotation where frame_id=?",(frame_id))
        # result = {'data': [dict(zip(tuple (query.keys()) ,i)) for i in query.cursor]}
        # return result
    
api.add_resource(Calculation_Assets, '/API/v1/calc_assets/<int:id>')  # bind url identifier to class; also make it querable



@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

if __name__ == '__main__':
    app.run(host='0.0.0.0')