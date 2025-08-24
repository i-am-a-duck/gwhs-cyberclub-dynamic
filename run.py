from app import create_app, db
from app.models import User
from app.security import hash_password, new_totp_secret
from flask.cli import with_appcontext
import click

app = create_app()

@app.cli.command("create-admin")
@with_appcontext
@click.argument("email")
@click.argument("password")
def create_admin(email, password):
    """Create an admin user with TOTP secret printed once."""
    u = User.query.filter_by(email=email).first()
    if u:
        click.echo("User exists.")
        return
    u = User(email=email.lower().strip(), name="Admin", password_hash=hash_password(password), is_admin=True, totp_secret=new_totp_secret())
    db.session.add(u); db.session.commit()
    click.echo(f"Created admin {email}. TOTP secret (store in your Authenticator app): {u.totp_secret}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=False)
