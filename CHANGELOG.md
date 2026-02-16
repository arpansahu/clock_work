# Changelog

## [3.0.0] - 2026-02-17
### Major Changes
- **Django 4.2.28 LTS Upgrade**: Migrated from Django 3.2.13 to 4.2.28 LTS with 75 package upgrades
- **Kubernetes Deployment**: Full production deployment on K3s with health probes and auto-restart
- **Jenkins CI/CD Pipeline**: Automated build and deployment with environment variable centralization
- **Django Channels HTTP Fix**: Added missing HTTP handler to ASGI routing (resolved HTTP 500 errors)

### Infrastructure Improvements
- Added custom `AllowedHostsWithSubnet` class supporting CIDR notation (10.42.0.0/16) for K8s pod network
- Production security: HSTS (1 year), SSL redirect, secure cookies, referrer policy
- Dynamic CSRF_TRUSTED_ORIGINS using PROTOCOL and DOMAIN environment variables
- Health probes: liveness (60s delay) and readiness (30s delay)
- Docker fail-fast error handling with `set -e`
- Harbor private Docker registry integration at harbor.arpansahu.space

### CI/CD Enhancements
- Fixed deployment job trigger name (clock_work_deploy)
- Fixed IMAGE_TAG variable scoping (26 env. prefix additions)
- Skipped build handling: intelligent image tag retrieval from build descriptions
- Health check accepts HTTP 301 redirect (SECURE_SSL_REDIRECT)
- JSON parsing without shell escaping issues

### Testing
- All 161 tests passing locally (70.7s) and Jenkins CI (77.1s)
- Browser UI tests with Playwright
- WebSocket integration tests
- Service health check management commands

### Code Quality
- Added subprocess and ipaddress imports
- Removed unused dependencies (RabbitMQ, Kafka, Elasticsearch)
- Cleaned up dummy files and old virtual environments
- Updated .gitignore for better exclusions
- Improved error handling and logging

### Documentation
- Updated README with current deployment architecture
- Added diagnostic scripts for troubleshooting
- Comprehensive deployment guides
- Jenkins pipeline documentation

## [2.0.0] - 2026-02-13
### Changed
- Updated database schema to use PostgreSQL with clock_work schema
- Updated domain configuration to clock-work.arpansahu.space
- Updated email configuration to admin@arpansahu.space
- Fixed dependency conflicts (typing_extensions, psycopg2-binary)
- Updated service health check commands
- Improved documentation and README structure

### Added
- Superuser account (admin/showmecode)
- Production database schema setup
- Enhanced service monitoring capabilities

## [1.0.0] - 2024-06-27
### Added
- Initial release of the project.
- User authentication module.