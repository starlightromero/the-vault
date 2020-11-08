"""Import libraries."""
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_admin import Admin
from the_vault.config import Config
from the_vault.admin import RestrictedAdminIndexView

db = SQLAlchemy()
admin = Admin(template_mode="bootstrap4")
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = "users.login"
login_manager.session_protection = "strong"


def create_app(config_class=Config):
    """Create an instance of the vault app."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    bcrypt.init_app(app)
    login_manager.init_app(app)
    admin.init_app(app, index_view=RestrictedAdminIndexView())

    from the_vault.main.routes import main
    from the_vault.users.routes import users

    app.register_blueprint(main)
    app.register_blueprint(users)

    with app.app_context():
        db.create_all()

    return app
