from crudFlaskMongodb.routes.index import *

from crudFlaskMongodb.models.user import User
from crudFlaskMongodb.forms.update_account_form import UpdateAccountForm

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
