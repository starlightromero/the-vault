"""Import libraries."""
from flask import redirect, url_for
from flask_admin import AdminIndexView
from flask_login import current_user


class RestrictedAdminIndexView(AdminIndexView):
    """Admin view custom class."""

    def is_accessible(self):
        """Return True is current user is authenticated."""
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        """Redirect user to login if not authenticated."""
        return redirect(url_for("users.login"))
