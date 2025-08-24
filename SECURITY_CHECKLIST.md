# Hardening Checklist

- [ ] Change SECRET_KEY and DB password in production.
- [ ] Enable TOTP for all admin users.
- [ ] Set `force_https=True` in Talisman when TLS is active end‑to‑end.
- [ ] Firewall: expose only 80/443; do not expose 5432.
- [ ] Regular patching: `docker compose pull` and rebuild.
- [ ] Offsite DB backups with retention.
- [ ] HSTS (Caddy adds when HTTPS is active); consider adding preload after testing.
- [ ] Fail2ban / Crowdsec on the host.
- [ ] Monitoring & log aggregation.
