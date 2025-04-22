from unittest import TestCase
from app import app
from models import db, User

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['TESTING'] = True
app.config['SQLALCHEMY_ECHO'] = False

class UserViewsTestCase(TestCase):
    """Tests for views for Users."""

    def setUp(self):
        """Clean up existing users & add test data."""
        with app.app_context():
            db.drop_all()
            db.create_all()

            user = User(first_name="Test", last_name="User", image_url="https://example.com/image.jpg")
            db.session.add(user)
            db.session.commit()

            self.test_user_id = user.id

    def tearDown(self):
        """Clean up fouled transactions."""
        with app.app_context():
            db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test User", html)

    def test_user_detail(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.test_user_id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Test User", html)

    def test_add_user(self):
        with app.test_client() as client:
            data = {"first_name": "New", "last_name": "Person", "image_url": ""}
            resp = client.post("/users/new", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("New Person", html)

    def test_edit_user(self):
        with app.test_client() as client:
            data = {"first_name": "Edited", "last_name": "User", "image_url": ""}
            resp = client.post(f"/users/{self.test_user_id}/edit", data=data, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn("Edited User", html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(f"/users/{self.test_user_id}/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn("Test User", html)

    def test_user_detail_not_found(self):
        """Test that requesting a non-existent user returns 404"""
        with app.test_client() as client:
            resp = client.get("/users/9999")
            self.assertEqual(resp.status_code, 404)

    def test_edit_user_cancel_redirect(self):
        """Test cancel button redirects to user detail"""
        with app.test_client() as client:
            resp = client.get(f"/users/{self.test_user_id}/edit")
            html = resp.get_data(as_text=True)

            self.assertIn(f'href="/users/{self.test_user_id}"', html)
