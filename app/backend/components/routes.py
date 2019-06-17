from components import app

from flask import Flask, render_template, flash, redirect, url_for, request
from typing import List, Dict
#from components.forms import LoginForm
#from flask_login import current_user, login_user, logout_user, login_required
# from components.models import User
# from werkzeug.urls import url_parse



# def favorite_colors() -> List[Dict]:
#     config = {
#         'user': 'root',
#         'password': 'root',
#         'host': '127.0.0.1', #'db',
#         'port': '32000', #'3306',
#         'database': 'knights'
#     }
#     connection = mysql.connector.connect(**config)
#     cursor = connection.cursor()
#     cursor.execute('SELECT * FROM favorite_colors')
#     results = [{name: color} for (name, color) in cursor]
#     cursor.close()
#     connection.close()

#     return results

@app.route('/setupdb')
def setupdb() -> str:
    db.create_all()
    admin = User(username='admin', email='admin@example.com')
    guest = User(username='guest', email='guest@example.com')
    db.session.add(admin)
    db.session.add(guest)
    db.session.commit()
    return "db setup"




@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        flash('Login requested for user {}, remember_me={}'.format(
            form.username.data, form.remember_me.data))
        return redirect('/index')
    return render_template('login.html', title='Sign In', form=form)

# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('index'))
#     form = LoginForm()
#     if form.validate_on_submit():
#         user = User.query.filter_by(username=form.username.data).first()
#         if user is None or not user.check_password(form.password.data):
#             flash('Invalid username or password')
#             return redirect(url_for('login'))
#         login_user(user, remember=form.remember_me.data)
#         next_page = request.args.get('next')
#         if not next_page or url_parse(next_page).netloc != '':
#             next_page = url_for('index')
#         return redirect(next_page)
#     return render_template('login.html', title='Sign In', form=form)

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))

# @app.route('/colors')
# def fav_colors() -> str:
#     return json.dumps({'favorite_colors': favorite_colors()})



@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username': 'Miguel'}
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home',  user=user, posts=posts)
