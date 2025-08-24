from flask import Blueprint, render_template, redirect, url_for, request, flash, session
from flask_login import login_user, login_required, logout_user
from ..models import User
from .. import db, login_manager
from ..security import hash_password, verify_password, new_totp_secret, verify_totp

bp = Blueprint("auth", __name__)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email","").strip().lower()
        password = request.form.get("password","")
        user = User.query.filter_by(email=email).first()
        if not user or not verify_password(user.password_hash, password):
            flash("Invalid credentials", "error")
            return render_template("auth/login.html")
        session["pre_2fa_user"] = user.id
        if user.totp_secret:
            return redirect(url_for("auth.totp"))
        login_user(user, remember=True)
        return redirect(url_for("admin.dashboard"))
    return render_template("auth/login.html")

@bp.route("/totp", methods=["GET", "POST"])
def totp():
    uid = session.get("pre_2fa_user")
    if not uid:
        return redirect(url_for("auth.login"))
    user = User.query.get(int(uid))
    if request.method == "POST":
        token = request.form.get("token","")
        if user and user.totp_secret and verify_totp(user.totp_secret, token):
            login_user(user, remember=True)
            session.pop("pre_2fa_user", None)
            return redirect(url_for("admin.dashboard"))
        else:
            flash("Invalid code", "error")
    return render_template("auth/totp.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("public.home"))
