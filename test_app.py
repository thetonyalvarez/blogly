from unittest import TestCase

from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_db'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class UserViewsTestCase(TestCase):
    """Tests for views for User."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()

        user = User(first_name="test_f", last_name="test_l",
                    image_url="https://cdn.pixabay.com/photo/2014/06/03/19/38/road-sign-361514_960_720.png")
        db.session.add(user)
        db.session.commit()

        self.user_id = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_show_users_redirect(self):
        with app.test_client() as client:
            resp = client.get('/')

            self.assertEqual(resp.status_code, 302)

    def test_show_users_followed(self):
        with app.test_client() as client:
            resp = client.get("/", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test_f', html)

    def test_show_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('test_f', html)

    def test_add_user(self):
        with app.test_client() as client:
            resp = client.get("/users/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<p>First Name:', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<h1 class="user-name">test_f', html)

    def test_handle_edit_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<input name="firstName" value="test_f"', html)

    def handle_delete_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn(
                '<input name="firstName" value="test_f"', html)


class PostViewsTestCase(TestCase):
    """Tests for views for Posts."""

    def setUp(self):
        """Add sample user."""

        User.query.delete()
        Post.query.delete()

        user = User(first_name="test_f", last_name="test_l",
                    image_url="https://cdn.pixabay.com/photo/2014/06/03/19/38/road-sign-361514_960_720.png")

        db.session.add(user)
        db.session.commit()

        self.user_id = user.id
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.image_url = user.image_url

        post = Post(title="test_title", content="test_content",
                    user_id=self.user_id)

        db.session.add(post)
        db.session.commit()

        self.post_id = post.id
        self.title = post.title
        self.content = post.content

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()

    def test_show_user_new_post_form(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user_id}/posts/new")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                'Add Post for test_f', html)
            self.assertNotIn(
                'Add Post for test_fddd', html)

    def test_handle_user_new_post(self):
        with app.test_client() as client:
            data = {
                'title-input': self.title,
                'content-input': self.content
            }

            resp = client.post(
                f"/users/{self.user_id}/posts/new", data=data)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

    def test_handle_user_new_post_followed(self):
        with app.test_client() as client:
            data = {
                'title-input': self.title,
                'content-input': self.content
            }

            resp = client.post(
                f"/users/{self.user_id}/posts/new", data=data, follow_redirects=True)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1 class="user-name">test_f', html)
            self.assertNotIn('<h1 class="user-name">test_fdddd', html)

    def test_show_single_post(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                '<p class="single-post-content">test_content', html)
            self.assertNotIn(
                '<p class="single-post-content">test_contentjsdkflasdf', html)

    def test_show_edit_post_form(self):
        with app.test_client() as client:
            resp = client.get(f"/posts/{self.post_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn(
                f'<input name="content-input" value="{self.content}"', html)

    def test_handle_edit_post(self):
        with app.test_client() as client:
            data = {
                'title-input': self.title,
                'content-input': self.content
            }

            resp = client.post(
                f"/posts/{self.user_id}/edit", data=data)

            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)

    def test_handle_delete_post(self):
        with app.test_client() as client:
            resp = client.post(f"/posts/{self.post_id}/delete")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 302)
            self.assertNotIn(
                '<input name="firstName" value="test_f"', html)
