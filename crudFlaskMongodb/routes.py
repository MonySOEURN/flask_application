import os
import secrets
from PIL import Image
from flask import Flask, render_template, url_for, flash, redirect, jsonify, request
from werkzeug.security import generate_password_hash, check_password_hash
from crudFlaskMongodb import app, db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

from crudFlaskMongodb.forms import RegistrationForm, LoginForm, UpdateAccountForm
from crudFlaskMongodb.models import User, Post

posts = [
    {
        'author': 'SOEURN Mony',
        'title': 'Blog post 1',
        'content': 'First Post content',
        'date_posted': 'May 22, 2020',
    },
    {
        'author': 'FOUR Year',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'May 23, 2020',
    },
]

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')

@app.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        user.save(user)
        flash('Your account has been created! You are now beable to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', title= 'Register', form=form)


@app.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        # made change here
        user = User.objects().filter(email=form.email.data).first() 
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title= 'Login', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))

def save_image_file(form_image_file, current_user_profile):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_image_file.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    if current_user_profile != 'default.jpg':
        current_file = os.path.join(app.root_path, 'static/profile_pics/')
        os.remove(current_file + current_user_profile)
    
    # working as resize the image
    output_size = (125, 125)
    i = Image.open(form_image_file)
    i.thumbnail(output_size)
    i.save(picture_path)
    
    # form_image_file.save(picture_path)
    return picture_fn

@app.route('/account', methods = ['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():


        # solve user account update problem using pymongo in flast-login
        user = User.objects().filter(username = current_user.username, email=current_user.email).first()
        current_user.username = form.username.data
        current_user.email = form.email.data 
        if user: 
            # solve update profile picture of user using pymongo
            if form.image_file.data:
                picture_file = save_image_file(form.image_file.data, current_user.image_file)
                current_user.image_file = picture_file
                user.update(username=form.username.data, email=form.email.data, image_file=picture_file)
            else:
                user.update(username=form.username.data, email=form.email.data)
            # solve update problem using pymongo in flast-login
            flash('Your account has been updated!', 'success')
            return redirect(url_for('account'))
    elif request.method == 'GET': 
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title= 'Account', image_file = image_file, form = form)


# ------------------------------------------------