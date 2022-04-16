"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def redirect_to_users():
    """Redirect to list of users."""

    return redirect("/users")


@app.route("/users")
def list_users():
    """Show all users."""

    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template("list.html", users=users)


@app.route('/users/new')
def show_add_user():
    """Show form to add new user."""

    return render_template("add-user.html")


@app.route('/users/new', methods=['POST'])
def handle_add_user():
    """Process the add form, adding a new user and going back to /users"""

    first_name = request.form['firstName']
    last_name = request.form['lastName']
    image_url = request.form['imageUrl'] if request.form['imageUrl'] else ''

    user = User(first_name=first_name,
                last_name=last_name, image_url=image_url)

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show information about the given user."""

    user = User.query.get_or_404(user_id)

    posts = Post.query.filter_by(user_id=Post.user_id)

    return render_template("show-user.html", user=user, posts=posts)


@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """Show the edit page for a user."""

    user = User.query.get_or_404(user_id)
    return render_template("edit-user.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def handle_edit_user(user_id):
    """Process the edit form, returning the user to the / users page."""

    user = User.query.get(user_id)

    user.first_name = request.form['firstName']
    user.last_name = request.form['lastName']
    user.image_url = request.form['imageUrl'] if request.form['imageUrl'] else ''

    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def handle_delete_user(user_id):
    """Delete the user."""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")


# Blog post routes
@app.route('/users/<int:user_id>/posts/new')
def show_user_new_post_form(user_id):
    """Show form to add a post for that user."""

    user = User.query.get_or_404(user_id)

    return render_template("/add-post.html", user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def handle_user_new_post(user_id):
    """Handle add form by user."""

    title = request.form['title-input']
    content = request.form['content-input']

    post = Post(title=title, content=content, user_id=user_id)

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_single_post(post_id):
    """Show a post."""

    post = Post.query.filter_by(id=post_id).one()

    return render_template("/show-post.html", post=post)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show form to edit a post"""

    post = Post.query.get(post_id)

    return render_template("/edit-post.html", post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handle_edit_post(post_id):
    """Handle editing of a post"""

    post = Post.query.get(post_id)

    post.title = request.form['title-input']
    post.content = request.form['content-input']

    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def handle_delete_post(post_id):
    """Delete the post."""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect("/users")
