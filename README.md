# GWHS Cybersecurity Club — Dynamic Site (Flask + Postgres + 2FA + Docker)

A secure, modular website with admin login (email/password + TOTP 2FA), CRUD for Events/Posts/Resources, CSP/headers, rate limiting, and a Docker stack (Caddy TLS + Postgres).

## Quick start (Docker)

```bash
cp .env.example .env
# edit .env (set a strong SECRET_KEY)

docker compose up -d --build

# init database
docker compose exec web flask db init
docker compose exec web flask db migrate -m "init"
docker compose exec web flask db upgrade

# create admin (TOTP secret will be printed once)
docker compose exec web flask create-admin admin@example.com "StrongPassword123!"
```
If you set your domain in `Caddyfile` and point DNS A/AAAA to this server, Caddy will fetch certificates automatically. Then open `https://<your-domain>/`.

## Local dev (no Docker)

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
export FLASK_APP=run.py
export DATABASE_URL="sqlite:///instance/app.db"
flask db init && flask db migrate -m "init" && flask db upgrade
flask create-admin admin@example.com "StrongPassword123!"
python run.py
# open http://localhost:8000
```

## second time run(no Docker)
    .\.venv\Scripts\Activate

    $env:FLASK_APP = "run.py"
$env:ENV = "dev"               # 本地调试时关闭 Secure Cookie
# 如果你还没在 __init__.py 里写默认 SQLite 路径，可以额外指定数据库：
# $env:DATABASE_URL = "sqlite:///" + ($pwd.Path + "\instance\app.db").Replace('\','/')

    python run.py

## Security choices

- Password hashing (Werkzeug), cookies Secure/HttpOnly/SameSite.
- TOTP 2FA (pyotp) for admin users.
- CSRF protection (Flask‑WTF), rate limiting (Flask‑Limiter), CSP/headers (Flask‑Talisman).
- Reverse proxy with Caddy for automatic HTTPS and HSTS.
- Postgres in production; SQLite fine for dev.

## Content model

- **Events**: title, start/end, location, notes, signup, gallery
- **Posts**: title, slug, body
- **Resources**: title, url, tier (beginner/intermediate/advanced/community)

## Next steps / Phase 2

- Markdown editor & public post pages by slug.
- Google / School SSO (OAuth 2.0) to replace passwords.
- Image uploads to S3/R2 + CDN.
- Audit logs for admin actions.
- Nightly DB backups.
