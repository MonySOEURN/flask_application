import os
import secrets
from PIL import Image
from flask import url_for, render_template
from flask_mail import Message
from crudFlaskMongodb import app, mail


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


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender = 'noreply@demo.com', recipients = [user.email])
    reset_password_link = url_for('users.reset_token', token = token, _external = True)
    msg.body = f'''To reset your password, please visit the following link:
    {reset_password_link}

    if you did not make this request then simple=y ignore this email and no changes will be make.
    '''
    msg.html = render_template('template_mail.html', reset_password_link = reset_password_link)
    mail.send(msg)