from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from flask_migrate import Migrate
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
from flask_talisman import Talisman
from werkzeug.middleware.proxy_fix import ProxyFix
from flask_wtf.csrf import CSRFProtect, generate_csrf
import os

db = SQLAlchemy()
login_manager = LoginManager()
csrf = CSRFProtect()
migrate = Migrate()

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    app.config.from_mapping(
        SECRET_KEY=os.environ.get("SECRET_KEY", "dev-not-secure"),
        SQLALCHEMY_DATABASE_URI=os.environ.get("DATABASE_URL", "sqlite:///instance/app.db").replace("postgres://", "postgresql://"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SESSION_COOKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE="Lax",
        REMEMBER_COOKIE_SECURE=True,
        WTF_CSRF_TIME_LIMIT=None,
    )

    if os.environ.get("ENV") == "dev":
        app.config.update(
            SESSION_COOKIE_SECURE=False,
            REMEMBER_COOKIE_SECURE=False,
    )


    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_port=1, x_prefix=1)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)
    migrate.init_app(app, db)

    limiter = Limiter(get_remote_address, app=app, default_limits=["200 per hour", "20 per minute"])

    csp = {
        'default-src': "'self'",
        'img-src': "'self' data:",
        'style-src': "'self' 'unsafe-inline'",
        'script-src': "'self'",
        'font-src': "'self' data:",
        'frame-ancestors': "'none'",
        'base-uri': "'self'",
        'form-action': "'self'",
    }
    Talisman(app, content_security_policy=csp, force_https=False)

    app.jinja_env.globals.update(csrf_token=generate_csrf)

    from .blueprints.public import bp as public_bp
    from .blueprints.auth import bp as auth_bp
    from .blueprints.admin import bp as admin_bp

    app.register_blueprint(public_bp)
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(admin_bp, url_prefix="/admin")

    @app.context_processor
    def inject_now():
        import datetime as _dt
        return {"year_now": _dt.datetime.now().year}

    return app
