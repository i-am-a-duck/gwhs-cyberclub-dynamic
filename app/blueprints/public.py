from flask import Blueprint, render_template
from ..models import Event, Post, Resource
from datetime import datetime

bp = Blueprint("public", __name__)

@bp.route("/")
def home():
    next_event = Event.query.filter(Event.start >= datetime.utcnow()).order_by(Event.start.asc()).first()
    posts = Post.query.order_by(Post.published_at.desc()).limit(3).all()
    return render_template("home.html", next_event=next_event, posts=posts)

@bp.route("/about")
def about():
    return render_template("about.html")

@bp.route("/events")
def events():
    upcoming = Event.query.filter(Event.start >= datetime.utcnow()).order_by(Event.start.asc()).all()
    past = Event.query.filter(Event.start < datetime.utcnow()).order_by(Event.start.desc()).all()
    return render_template("events.html", upcoming=upcoming, past=past)

@bp.route("/resources")
def resources():
    res = Resource.query.order_by(Resource.tier.asc(), Resource.title.asc()).all()
    return render_template("resources.html", resources=res)

@bp.route("/join")
def join():
    return render_template("join.html")

@bp.route("/policies")
def policies():
    return render_template("policies.html")

@bp.route("/contact")
def contact():
    return render_template("contact.html")


