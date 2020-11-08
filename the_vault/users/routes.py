"""Import libraries."""
from flask import render_template, Blueprint, redirect, url_for, flash
from flask_login import login_required, current_user, login_user, logout_user
from the_vault import db
from the_vault.models import User
from the_vault.users.forms import (
    RegistrationForm,
    LoginForm,
    UpdateAccountForm,
)

users = Blueprint("users", __name__)


@users.route("/login", methods=["GET", "POST"])
def login():
    """Show login page."""
    if current_user.is_authenticated:
        redirect(url_for("main.home"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            db.session.commit()
            return redirect(url_for("users.account"))
        flash("Login Unsuccessful. Please verify email and password.")
    return render_template("login.html.j2", form=form)


@users.route("/register", methods=["GET", "POST"])
def register():
    """Show register page."""
    if current_user.is_authenticated:
        redirect(url_for("main.home"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data)
        user.check_admin()
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Your account has been created! You are now able to log in.")
        return redirect(url_for("users.login"))
    return render_template("register.html.j2", form=form)


@users.route("/account")
@login_required
def account():
    """Show account page."""
    form = UpdateAccountForm()
    user = User.query.filter_by(email=current_user.email).first_or_404()
    if form.validate_on_submit():
        current_user.email = form.username.data
        db.session.commit()
        flash("Your account has been updated!")
        return redirect(url_for("users.account"))
    form.email.data = current_user.email
    return render_template("account.html.j2", form=form, user=user)


@users.route("/logout")
@login_required
def logout():
    """Logout user and redirect to home page."""
    logout_user()
    return redirect(url_for("main.home"))
