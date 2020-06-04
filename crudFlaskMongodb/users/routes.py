from flask import Blueprint, render_template, url_for, flash, redirect, request
from flask_login import login_user, logout_user, current_user, login_required
from crudFlaskMongodb import db, bcrypt
from crudFlaskMongodb.models.user import User
from crudFlaskMongodb.models.post import Post
from crudFlaskMongodb.users.forms import (  ResetPasswordForm, LoginForm, UpdateAccountForm, 
                                            ResetPasswordForm, RequestResetForm, RegistrationForm )
from crudFlaskMongodb.users.utils import save_image_file, send_reset_email


users = Blueprint('users', __name__)


@users.route('/register', methods = ['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        user.save(user)
        flash('Your account has been created! You are now beable to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('register.html', title= 'Register', form=form)


@users.route('/login', methods = ['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = LoginForm()
    if form.validate_on_submit():
        # made change here
        user = User.objects().filter(email=form.email.data).first() 
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember = form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('main.home'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title= 'Login', form=form)


@users.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route('/account', methods = ['GET', 'POST'])
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
            return redirect(url_for('users.account'))
    elif request.method == 'GET': 
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename = 'profile_pics/' + current_user.image_file)
    return render_template('account.html', title= 'Account', image_file = image_file, form = form)


@users.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)

    # get the post in descending order
    user = User.objects().filter(username = username).first_or_404()
    posts = Post.objects.filter(author = user)\
            .order_by("-date_posted")\
            .paginate(page=page, per_page=5)
    return render_template('posts/user_posts.html', posts=posts, user=user)


@users.route('/reset_password', methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.objects().filter(email = form.email.data).first()
        send_reset_email(user)
        flash('An Email has been sent with instructions to reset password', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title= 'Reset Password', form=form)


@users.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an Invalid or Expired token', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.update(password = hashed_password)
        flash('Your password has been updated! You are now beable to log in.', 'success')
        return redirect(url_for('users.login'))
    return render_template('reset_token.html', title= 'Reset Password', form=form)