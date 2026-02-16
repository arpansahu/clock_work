# Security Policy


## Supported Versions

We provide security patches for the latest release of our project. Users are encouraged to always update to the latest version to ensure they have the most recent security fixes.

| Version       | Supported          |
| ------------- | ------------------ |
| 3.0.0 (Latest)| ✅ Django 4.2.28 LTS |
| 2.0.0         | ✅ Security updates only |
| 1.0.0         | ❌ No longer supported |
| Older versions| ❌ Not supported    |

### Current Production Stack (v3.0.0)

- **Django**: 4.2.28 LTS (Long Term Support until April 2026)
- **Python**: 3.10.7
- **Security Features**:
  - HSTS enabled (1 year max-age)
  - Secure SSL redirect (SECURE_SSL_REDIRECT=True)
  - Secure cookies (SESSION_COOKIE_SECURE, CSRF_COOKIE_SECURE)
  - X-Frame-Options: DENY
  - Referrer-Policy: strict-origin-when-cross-origin
  - Custom ALLOWED_HOSTS with CIDR support
  - Django Channels with secure WebSocket support
  - TLS-enabled Redis connection (rediss://)
  - SCRAM-SHA-256 PostgreSQL authentication
  - Sentry error monitoring and tracking

## Reporting a Vulnerability

If you find a security vulnerability, please send an email to [admin@arpansahu.space](mailto:admin@arpansahu.space). Please include the following details with your report:

- A description of the vulnerability
- Steps to reproduce the issue
- The impact of the vulnerability (e.g., what data can be accessed, modified, or deleted)

### Response Time

We will respond to your report within 48 hours and provide a detailed report within 5 days.

### Handling Vulnerabilities

Once a vulnerability is reported, the following steps will be taken:

1. **Acknowledgment**: We will acknowledge receipt of the vulnerability report.
2. **Investigation**: We will investigate the vulnerability and determine its impact.
3. **Fix Development**: We will develop a fix for the vulnerability.
4. **Patch Release**: We will release a patch for the supported versions listed above.
5. **Public Disclosure**: We will publicly disclose the vulnerability and the fix once the patch is released.

## Security Best Practices

We encourage our users to follow these best practices to secure their deployment:

- Keep your software up to date.
- Use strong, unique passwords for different accounts.
- Enable two-factor authentication (2FA) where possible.
- Regularly review and update your security settings.

## Contact

For any security-related questions, please contact us at [admin@arpansahu.space](mailto:admin@arpansahu.space).

## Credits

We thank the following individuals for responsibly reporting vulnerabilities to us: