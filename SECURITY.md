# Security Policy

## Reporting a Vulnerability

If you discover a security vulnerability in TextMine, please follow responsible disclosure practices:

1. **Do NOT** open a public GitHub issue
2. Email the maintainers with details about the vulnerability
3. Include steps to reproduce if possible
4. Allow time for the maintainers to address the issue before public disclosure

## Security Considerations

### API Keys & Secrets
- **Never** commit `.env` files to version control
- Use `.env.example` as a template
- Rotate API keys regularly
- Use environment variables in production

### File Uploads
- Validate file types and sizes
- Scan uploaded files for malware
- Store uploaded files securely
- Clean up temporary files after processing
- Implement rate limiting in production

### Dependencies
- Keep dependencies updated
- Monitor for security advisories
- Review dependency licenses
- Use tools like `pip-audit` to check for vulnerabilities

## Deployment Security

### Production Recommendations
1. Use HTTPS/TLS for all API communications
2. Implement authentication and authorization
3. Rate limit API endpoints
4. Use secrets management (AWS Secrets Manager, HashiCorp Vault, etc.)
5. Monitor logs for suspicious activity
6. Keep servers patched and updated
7. Use containerization (Docker) with security best practices

### Example Production Deployment
```bash
# Use gunicorn with HTTPS
gunicorn main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000 \
  --ssl-keyfile /path/to/key.pem \
  --ssl-certfile /path/to/cert.pem
```

## Supported Versions

| Version | Status | Support |
|---------|--------|---------|
| 2.x | Active | Actively maintained |
| 1.x | Deprecated | Security fixes only |

## Additional Resources

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [FastAPI Security](https://fastapi.tiangolo.com/tutorial/security/)
- [Python Security Best Practices](https://python-security.readthedocs.io/)

Thank you for helping keep TextMine secure! 🔒
