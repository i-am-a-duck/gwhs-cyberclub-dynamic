from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from ..models import Event, Post, Resource, User
from .. import db
from datetime import datetime
from slugify import slugify

bp = Blueprint("admin", __name__)

def admin_required():
    return current_user.is_authenticated and current_user.is_admin

@bp.before_request
def check_admin():
    if not request.endpoint:
        return
    if request.blueprint == "admin":
        if not admin_required():
            return redirect(url_for("auth.login"))

@bp.route("/")
@login_required
def dashboard():
    if not admin_required():
        return redirect(url_for("auth.login"))
    stats = {
        "events": Event.query.count(),
        "posts": Post.query.count(),
        "resources": Resource.query.count(),
        "users": User.query.count(),
    }
    return render_template("admin/dashboard.html", stats=stats)

@bp.route("/events/new", methods=["GET","POST"])
@login_required
def events_new():
    if request.method == "POST":
        ev = Event(
            title=request.form["title"],
            start=datetime.fromisoformat(request.form["start"]),
            end=datetime.fromisoformat(request.form["end"]) if request.form.get("end") else None,
            location=request.form.get("location"),
            notes=request.form.get("notes"),
            signup=request.form.get("signup"),
            gallery=request.form.get("gallery"),
        )
        db.session.add(ev); db.session.commit()
        flash("Event created","ok")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/events_form.html", ev=None)

@bp.route("/events/<int:ev_id>/edit", methods=["GET","POST"])
@login_required
def events_edit(ev_id):
    ev = Event.query.get_or_404(ev_id)
    if request.method == "POST":
        ev.title=request.form["title"]
        ev.start=datetime.fromisoformat(request.form["start"])
        ev.end=datetime.fromisoformat(request.form["end"]) if request.form.get("end") else None
        ev.location=request.form.get("location")
        ev.notes=request.form.get("notes")
        ev.signup=request.form.get("signup")
        ev.gallery=request.form.get("gallery")
        db.session.commit()
        flash("Event updated","ok")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/events_form.html", ev=ev)

@bp.route("/events/<int:ev_id>/delete", methods=["POST"])
@login_required
def events_delete(ev_id):
    ev = Event.query.get_or_404(ev_id)
    db.session.delete(ev); db.session.commit()
    flash("Event deleted","ok")
    return redirect(url_for("admin.dashboard"))

@bp.route("/posts/new", methods=["GET","POST"])
@login_required
def posts_new():
    if request.method == "POST":
        title = request.form["title"]
        slug = slugify(request.form.get("slug") or title)
        post = Post(title=title, slug=slug, body=request.form["body"])
        db.session.add(post); db.session.commit()
        flash("Post created","ok")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/posts_form.html", post=None)

@bp.route("/posts/<int:pid>/edit", methods=["GET","POST"])
@login_required
def posts_edit(pid):
    post = Post.query.get_or_404(pid)
    if request.method == "POST":
        post.title = request.form["title"]
        post.slug = slugify(request.form.get("slug") or post.title)
        post.body = request.form["body"]
        db.session.commit()
        flash("Post updated","ok")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/posts_form.html", post=post)

@bp.route("/posts/<int:pid>/delete", methods=["POST"])
@login_required
def posts_delete(pid):
    post = Post.query.get_or_404(pid)
    db.session.delete(post); db.session.commit()
    flash("Post deleted","ok")
    return redirect(url_for("admin.dashboard"))

@bp.route("/resources/new", methods=["GET","POST"])
@login_required
def resources_new():
    if request.method == "POST":
        r = Resource(title=request.form["title"], url=request.form["url"], tier=request.form.get("tier"))
        db.session.add(r); db.session.commit()
        flash("Resource created","ok")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/resources_form.html", res=None)

@bp.route("/resources/<int:rid>/edit", methods=["GET","POST"])
@login_required
def resources_edit(rid):
    r = Resource.query.get_or_404(rid)
    if request.method == "POST":
        r.title=request.form["title"]; r.url=request.form["url"]; r.tier=request.form.get("tier")
        db.session.commit()
        flash("Resource updated","ok")
        return redirect(url_for("admin.dashboard"))
    return render_template("admin/resources_form.html", res=r)

@bp.route("/resources/<int:rid>/delete", methods=["POST"])
@login_required
def resources_delete(rid):
    r = Resource.query.get_or_404(rid)
    db.session.delete(r); db.session.commit()
    flash("Resource deleted","ok")
    return redirect(url_for("admin.dashboard"))
