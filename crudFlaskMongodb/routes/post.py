from crudFlaskMongodb.routes.index import *

from crudFlaskMongodb.forms.post_form import PostForm

@app.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        flash('Your Post has been created!', 'success')
        return redirect(url_for('home'))

    return render_template('posts/create_post.html', title= 'New Post', form=form)