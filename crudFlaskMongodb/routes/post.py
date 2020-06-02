from crudFlaskMongodb.routes.index import *

from crudFlaskMongodb.forms.post_form import PostForm
from crudFlaskMongodb.models.post import Post

@app.route('/post/new', methods = ['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        # bson.errors.InvalidDocument: cannot encode objectof type: <class 'werkzeug.local.LocalProxy'>
        # solve by using
        # _get_current_object()
        post = Post(title = form.title.data, content = form.content.data, author = current_user._get_current_object(), user_id = current_user.id)
        post.save(post)
        flash('Your Post has been created!', 'success')
        return redirect(url_for('home'))

    return render_template('posts/create_post.html', title= 'New Post', form=form)