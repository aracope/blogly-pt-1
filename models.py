"""Models for Blogly."""
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect database to Flask app."""
    db.app = app
    db.init_app(app)


class User(db.Model):
    """User model for Blogly"""

    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    image_url = db.Column(
        db.String,
        nullable=False,
        default="https://cdn-icons-png.flaticon.com/512/149/149071.png"
    )

    def __repr__(self):
        return f"<User id={self.id} name={self.first_name} {self.last_name}>"
    
    def get_full_name(self):
        """Return full name of user."""
        return f"{self.first_name} {self.last_name}"