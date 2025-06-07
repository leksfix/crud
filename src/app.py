from flask import Flask, render_template, request, url_for, abort
from repository import PostsRepository

app = Flask(__name__)

repo = PostsRepository(50)


@app.route('/')
def index():
    return render_template('index.html')


# BEGIN (write your solution here)
@app.route('/posts')
def posts_index():
    page = int(request.args.get('page', 1))
    posts = repo.content()[(page - 1) * 5: page * 5]
    return render_template(
        "posts/index.html",
        posts=posts,
        prev_page = f"{url_for('posts_index')}?page={max(page - 1, 1)}",
        next_page = f"{url_for('posts_index')}?page={page + 1}"
    )

@app.route('/posts/<slug>')
def posts_show(slug):
    post = repo.find(slug)
    if not post:
        abort(404)
    return render_template(
        "posts/show.html",
        post=post
    )


@app.errorhandler(404)
def not_found(error):
    return "Page not found", 404
# END
