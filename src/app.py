import os

from flask import (
    Flask,
    flash,
    get_flashed_messages,
    redirect,
    render_template,
    request,
    url_for,
)
from repository import PostsRepository
from validator import validate


app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')


@app.route('/')
def index():
    return render_template('index.html')


@app.get('/posts')
def posts_get():
    repo = PostsRepository()
    messages = get_flashed_messages(with_categories=True)
    posts = repo.content()
    return render_template(
        'posts/index.html',
        posts=posts,
        messages=messages,
        )


# BEGIN (write your solution here)
@app.get('/posts/new')
def posts_new():
    post = {}
    errors = []
    return render_template(
        'posts/new.html', 
        post=post, 
        errors=errors
        )

@app.post('/posts')
def posts_post():
    repo = PostsRepository()
    post = request.form.to_dict()
    errors = validate(post)
    if errors:
        return render_template(
            'posts/new.html', 
            post=post, 
            errors=errors
            ), 422
    repo.save(post)
    flash("Post has been created")
    return redirect(url_for("posts_get"))


# END
