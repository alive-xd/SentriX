# Changelog

All notable changes to SentriX are documented here.

## [1.0.0] - 2026-06-15

### Added
- Alert management system with severity filtering (CRITICAL / HIGH / MEDIUM / LOW)
- Case management with full incident timeline and artifact linking
- JWT authentication with Redis-backed refresh token rotation and logout blocklisting
- RBAC with granular role permissions (Admin, Analyst, Read-Only)
- Threat Intelligence module with AlienVault OTX and VirusTotal integration
- Malware Analysis with SHA256 tracking, threat score, and sandbox verdict display
- Threat Hunting with fast JSONB indexed querying over security telemetry
- SOAR playbook engine with ~120ms execution overhead
- AI Investigation Assistant backed by LLM reasoning for false positive triage
- Docker Compose single-command deployment
- Database seeding script generating ~1,000 realistic SOC records
- Full async Python stack (asyncio, asyncpg, httpx)
- Pydantic v2 input validation across all API endpoints
- OpenAPI / Swagger auto-generated docs at /docs

### Security
- bcrypt password hashing via passlib
- SQL injection protection via SQLAlchemy ORM parameterized queries
- TLS 1.3 termination guidance for production deployments
