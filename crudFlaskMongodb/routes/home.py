from crudFlaskMongodb.routes.index import *

from crudFlaskMongodb.models.post import Post 

@app.route('/')
@app.route('/home')
def home():
    page = request.args.get('page', 1, type=int)

    # working
    # posts = Post.objects.limit(5)
    # posts = Post.objects().limit(5)
    # posts = Post.objects().limit(5).all()
    # posts = Post.objects()
    # posts = Post.objects().skip(page).limit(5)
    # posts = Post.objects.skip(page).limit(5).all()

    posts = Post.objects.paginate(page=page, per_page=5)



    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')