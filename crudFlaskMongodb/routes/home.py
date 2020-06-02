from crudFlaskMongodb.routes.index import *

posts = [
    {
        'author': 'SOEURN Mony',
        'title': 'Blog post 1',
        'content': 'First Post content',
        'date_posted': 'May 22, 2020',
    },
    {
        'author': 'FOUR Year',
        'title': 'Blog post 2',
        'content': 'Second post content',
        'date_posted': 'May 23, 2020',
    },
]
 
@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html', posts=posts)

@app.route('/about')
def about():
    return render_template('about.html', title='About')