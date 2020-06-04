from crudFlaskMongodb.routes.index import *

from crudFlaskMongodb.forms.register_form import RegistrationForm
from crudFlaskMongodb.forms.login_form import LoginForm
from crudFlaskMongodb.forms.reset_password_form import ResetPasswordForm
from crudFlaskMongodb.forms.request_reset_form import RequestResetForm
from crudFlaskMongodb.models.user import User

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

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender = 'noreply@demo.com', recipients = [user.email])
    reset_password_link = url_for('reset_token', token = token, _external = True)
    msg.body = f'''To reset your password, please visit the following link:
    {reset_password_link}

    if you did not make this request then simple=y ignore this email and no changes will be make.
    '''
    msg.html = render_template('template_mail.html', reset_password_link = reset_password_link)
    mail.send(msg)

@app.route('/reset_password', methods = ['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.objects().filter(email = form.email.data).first()
        send_reset_email(user)
        flash('An Email has been sent with instructions to reset password', 'success')
        return redirect(url_for('login'))
    return render_template('reset_request.html', title= 'Reset Password', form=form)

@app.route('/reset_password/<token>', methods = ['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an Invalid or Expired token', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.update(password = hashed_password)
        flash('Your password has been updated! You are now beable to log in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title= 'Reset Password', form=form)

