"""Import libraries."""
from flask_login import UserMixin, current_user
from flask_admin.contrib.sqla import ModelView
from the_vault import db, login_manager, bcrypt, admin


@login_manager.user_loader
def load_user(user_id):
    """Get current logged in user."""
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    """User database model class."""

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=True, unique=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __repr__(self):
        """User returns email."""
        if self.is_admin:
            return f"Admin('{self.email}')"
        return f"User('{self.email}')"

    def set_password(self, password):
        """Set user's password as hash."""
        self.password = bcrypt.generate_password_hash(password).decode(
            "utf-8"
        )

    def check_password(self, password):
        """Check if given password matches hashed password."""
        return bcrypt.check_password_hash(self.password, password)

    def check_admin(self):
        """Check if user is authorized to be an admin."""
        if self.email == "admin@admin.com":
            self.is_admin = True


admin.add_view(ModelView(User, db.session))
