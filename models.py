"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class User(db.Model):
    """User."""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(25), nullable=False)
    last_name = db.Column(db.String(25), nullable=False)
    image_url = db.Column(db.String(255), nullable=False)

    posts = db.relationship("Post", backref="user",
                            cascade="all, delete-orphan")

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Post(db.Model):
    """Post."""

    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(80), nullable=False)
    content = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime,
                           nullable=False,
                           default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # user_rel = db.relationship(
    # 'User', backref='posts', cascade='all, delete-orphan')

    @property
    def cleaned_date(self):
        return self.created_at.strftime("%a %b %-d  %Y, %-I:%M %p")


class PostTag(db.Model):
    """Post Tag join table."""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True, nullable=False)
    tag_id = db.Column(db.Integer, db.ForeignKey(
        'tags.id'), primary_key=True, nullable=False)


class Tag(db.Model):
    """Tag."""

    __tablename__ = "tags"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        # cascade="all,delete",
        backref="tags",
    )


def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
