from crudFlaskMongodb.routes.index import *

from crudFlaskMongodb.forms.post_form import PostForm
from crudFlaskMongodb.models.post import Post
from crudFlaskMongodb.models.user import User

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

    return render_template('posts/create_post.html', title= 'New Post', form=form, legend='New Post')

@app.route("/post/<post_id>")
def post(post_id):
    post = Post.objects().filter(id = post_id).first()
    if post:
        return render_template('posts/post_detail.html', title=post.title, post= post)
    else:
        return render_template('404.html', title = '404 Not Found')

@app.route("/post/<post_id>/update", methods = ['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.objects().filter(id = post_id).first()
    if post.author.id != current_user.id:
        abort(403)
    if post is None:
        return render_template('404.html', title = '404 Not Found')
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.update(title=form.title.data, content=form.content.data)
        flash('Your Post has been updated!.', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == "GET":
        form.title.data = post.title
        form.content.data = post.content
    return render_template('posts/create_post.html', title= 'Update Post', form=form, legend='Update Post')

@app.route("/post/<post_id>/delete", methods = ['POST'])
@login_required
def delete_post(post_id):
    post = Post.objects().filter(id = post_id).first()
    if post.author.id != current_user.id:
        abort(403)
    if post is None:
        return render_template('404.html', title = '404 Not Found')
    else:
        post.delete()
        flash('You have successfully deleted post!.', 'success')
        return redirect(url_for('home'))


@app.route('/user/<string:username>')
def user_posts(username):
    page = request.args.get('page', 1, type=int)

    # get the post in descending order
    user = User.objects().filter(username = username).first_or_404()
    posts = Post.objects.filter(author = user)\
            .order_by("-date_posted")\
            .paginate(page=page, per_page=5)
    return render_template('posts/user_posts.html', posts=posts, user=user)
