from crudFlaskMongodb.routes.index import *

from crudFlaskMongodb.models.post import Post 

@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)

    # get the post in descending order
    posts = Post.objects.order_by("-date_posted").paginate(page=page, per_page=5)
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')