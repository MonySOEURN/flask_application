from crudFlaskMongodb.routes.index import *

from crudFlaskMongodb.models.post import Post 

@app.route('/')
@app.route('/home')
def home():
    posts = Post.objects()
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')