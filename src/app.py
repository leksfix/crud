from flask import (
    Flask,
    flash,
    get_flashed_messages,
    make_response,
    redirect,
    render_template,
    request,
    url_for,
)
import os

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


@app.route('/posts/new')
def new_post():
    post = {}
    errors = {}
    return render_template(
        'posts/new.html',
        post=post,
        errors=errors,
    )


@app.post('/posts')
def posts_post():
    repo = PostsRepository()
    data = request.form.to_dict()
    errors = validate(data)
    if errors:
        return render_template(
            'posts/new.html',
            post=data,
            errors=errors,
            ), 422
    id = repo.save(data)
    flash('Post has been created', 'success')
    resp = make_response(redirect(url_for('posts_get')))
    resp.headers['X-ID'] = id
    return resp


# BEGIN (write your solution here)
@app.get('/posts/<id>/update')
def post_update_get(id):
    repo = PostsRepository()
    data = repo.find(id)
    if not data:
        return "Page not found", 404
    errors = {}
    return render_template(
        'posts/edit.html',
        post=data,
        errors=errors
    )

@app.post('/posts/<id>/update')
def post_update(id):
    repo = PostsRepository()
    data = request.form.to_dict()
    post = repo.find(id)
    if not post:
        return "Page not found", 404
    post['title'] = data['title']
    post['body'] = data['body']
    errors = validate(post)
    if errors:
        return render_template(
            'posts/edit.html',
            post=post,
            errors=errors
        ), 422
    repo.save(post)
    flash('Post has been updated')
    return redirect(url_for('posts_get'))


@app.post('/posts/<id>/delete')
def post_delete(id):
    repo=PostsRepository()
    repo.destroy(id)
    flash('Post has been removed')
    return redirect(url_for('posts_get'))
    
# END
