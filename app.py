"""Blogly application."""

import re
from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag

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

    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()

    return render_template("/list-recent-posts.html", posts=posts)


@app.route("/users")
def list_users():
    """Show all users."""

    users = User.query.order_by(User.last_name, User.first_name).all()

    return render_template("list-user.html", users=users)


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

# #############################
# Blog post routes


@app.route('/posts')
def show_posts():
    """Show all posts."""

    return redirect("/")


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
    
    tag_ids = [int(num) for num in request.form.getlist("post-tag")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.add(post)
    db.session.commit()

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_single_post(post_id):
    """Show a post."""

    post = Post.query.get_or_404(post_id)
    
    return render_template("/show-post.html", post=post)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    """Show form to edit a post"""

    post = Post.query.get(post_id)
    tags = Tag.query.all()


    return render_template("/edit-post.html", post=post, tags=tags)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def handle_edit_post(post_id):
    """Handle editing of a post"""

    post = Post.query.get(post_id)
    post.title = request.form['title-input']
    post.content = request.form['content-input']
    
    tag_ids = [int(num) for num in request.form.getlist("post-tag")]
    post.tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

    db.session.commit()

    return redirect(f"/posts/{post_id}")


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def handle_delete_post(post_id):
    """Delete the post."""

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect("/users")


# #############################
# Tag routes
@app.route('/tags')
def show_tags():
    """Show all tags."""

    tags = Tag.query.all()

    return render_template("/list-tag.html", tags=tags)


@app.route('/tags/<int:tag_id>')
def show_single_tag(tag_id):
    """Show all tags."""

    tag = Tag.query.get_or_404(tag_id)

    return render_template("/show-tag.html", tag=tag)

@app.route('/tags/new', methods=['GET'])
def show_add_tag_form():
    """Shows a form to add a new tag."""
    
    return render_template("/add-tag.html")


@app.route('/tags/new', methods=['POST'])
def handle_add_tag_form():
    """Process add form, adds tag, and redirect to tag list."""
    
    new_tag = request.form['tag']
    
    tag = Tag(name=new_tag)

    db.session.add(tag)
    db.session.commit()
    
    return redirect("/tags")


@app.route('/tags/<int:tag_id>/edit', methods=['GET'])
def show_edit_tag_form(tag_id):
    """Show edit form for a tag."""

    tag = Tag.query.filter_by(id=tag_id).one()

    return render_template("/edit-tag.html", tag=tag)


@app.route('/tags/<int:tag_id>/edit', methods=['POST'])
def handle_edit_tag_form(tag_id):
    """Process edit form, edit tag, and redirects to the tags list."""

    tag = Tag.query.get(tag_id)

    tag.name = request.form["tag"]

    db.session.commit()

    return redirect("/tags")


@app.route('/tags/<int:tag_id>/delete', methods=['POST'])
def handle_delete_tag_form(tag_id):
    """Delete a tag."""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    return redirect("/tags")

