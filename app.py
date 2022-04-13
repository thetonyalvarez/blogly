"""Blogly application."""

from flask import Flask, request, redirect, render_template
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def list_users():
    """Redirect to list of users."""

    return redirect("/users")


@app.route("/users")
def list_users():
    """Show all users."""

    users = User.query.all()
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
    image_url = request.form['imageUrl'] if image_url else ''

    user = User(first_name, last_name, image_url)

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """Show information about the given user."""

    user = User.query.get_or_404(user_id)
    return render_template("show-user.html", user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_user(user_id):
    """Show the edit page for a user."""

    user = User.query.get_or_404(user_id)
    return redirect("edit-user.html", user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def handle_edit_user(user_id):
    """Process the edit form, returning the user to the / users page."""

    first_name = request.form['firstName']
    last_name = request.form['lastName']
    image_url = request.form['imageUrl'] if image_url else ''

    user = User(first_name, last_name, image_url)

    db.session.add(user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def handle_delete_user(user_id):
    """Delete the user."""

    user = User.query.get_or_404(user_id)

    db.session.delete(user)
    db.session.commit()

    return redirect("/users")
