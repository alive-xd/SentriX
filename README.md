<div align="center">
  <img src="assets/banner.png" alt="Sentrix Banner" width="100%" />

  <br />
  <br />

  <h1>🛡️ Sentrix Platform</h1>
  <p><strong>A Modern Open-Source Security Operations Center (SOC) Workspace</strong></p>

  <p>
    <a href="https://github.com/alive-xd/SentriX/stargazers">
      <img src="https://img.shields.io/github/stars/alive-xd/SentriX?style=flat-square&color=3b82f6" alt="GitHub Stars" />
    </a>
    <a href="https://github.com/alive-xd/SentriX/network/members">
      <img src="https://img.shields.io/github/forks/alive-xd/SentriX?style=flat-square&color=3b82f6" alt="GitHub Forks" />
    </a>
    <a href="https://github.com/alive-xd/SentriX/issues">
      <img src="https://img.shields.io/github/issues/alive-xd/SentriX?style=flat-square&color=3b82f6" alt="GitHub Issues" />
    </a>
  </p>

  <p>
    <a href="https://github.com/alive-xd/SentriX/actions/workflows/build.yml">
      <img src="https://img.shields.io/github/actions/workflow/status/alive-xd/SentriX/build.yml?branch=main&label=Build&style=flat-square&color=3b82f6" alt="Build Status" />
    </a>
    <a href="https://github.com/alive-xd/SentriX/blob/main/LICENSE">
      <img src="https://img.shields.io/github/license/alive-xd/SentriX?style=flat-square&color=3b82f6" alt="License" />
    </a>
    <a href="https://nextjs.org">
      <img src="https://img.shields.io/badge/Next.js-14+-black?style=flat-square&logo=next.js" alt="Next.js" />
    </a>
    <a href="https://fastapi.tiangolo.com">
      <img src="https://img.shields.io/badge/FastAPI-0.100+-009688?style=flat-square&logo=fastapi&logoColor=white" alt="FastAPI" />
    </a>
    <a href="https://www.postgresql.org/">
      <img src="https://img.shields.io/badge/PostgreSQL-16-4169E1?style=flat-square&logo=postgresql&logoColor=white" alt="PostgreSQL" />
    </a>
    <a href="https://redis.io/">
      <img src="https://img.shields.io/badge/Redis-7.0+-DC382D?style=flat-square&logo=redis&logoColor=white" alt="Redis" />
    </a>
  </p>

  <p>
    <strong>Designed using enterprise architecture patterns for modern blue teams.</strong>
  </p>
</div>

---

## 🌟 Overview

**Sentrix** is a modular, service-oriented Security Operations Center (SOC) workspace. 

Built using enterprise architecture patterns (Next.js App Router, FastAPI, PostgreSQL, and Redis), Sentrix provides a robust foundation for building advanced security workflows. It centralizes Alert Management, Threat Intelligence tracking, and Case Collaboration into a single, intuitive interface, providing developers and security teams with a highly extensible platform to build upon.

## 🏢 Use Cases

- **Development Foundation**: Implements a modular service-oriented backend perfect for building custom SOC solutions.
- **Incident Response Tooling**: Quickly deploy Sentrix into an environment using Docker to establish a central tracking workspace.
- **Cyber Range & Education**: Supports seeded datasets for realistic development and demonstrations, training junior analysts on incident response workflows.

## 📊 Project Statistics

| Metric | Verified Count |
| :--- | :--- |
| **Frontend Pages** | 29 |
| **REST API Endpoints** | 81 |
| **Database Tables** | 26 |
| **Backend Services** | 13 |
| **Seeded Alerts** | 485 |
| **Audit Log Entries** | 1000 |

## 🎯 Design Goals

1. **Modern Architecture**: Full asynchronous Python adoption (`asyncio`, `asyncpg`) backed by a strict Repository/Service pattern.
2. **Actionable Context**: Centralized dashboards linking Threat Intel and Malware metadata directly into Cases.
3. **Frictionless Deployment**: Zero complicated Kubernetes manifests required for initial deployment; just pure Docker Compose.
4. **Beautiful UX**: Sentrix leverages TailwindCSS, shadcn/ui, and Framer Motion for a premium dark-mode aesthetic.

---

## ✨ Current Capabilities

### ✅ Fully Implemented
- **Alert Management**: Full CRUD REST APIs and UI for managing security alerts.
- **Case Management**: Collaborate on incidents with dedicated timelines and artifact linking.
- **Authentication**: Stateless JWT lifecycle with Redis-backed refresh token blocklisting.
- **Audit Logging**: Comprehensive internal tracking of user actions.
- **Pagination & Filtering**: Standardized across major data grids.

### ⚠️ Partially Implemented
- **Basic Global Search**: Broad SQL `ILIKE` searches across primary entities.
- **Foundational Role-Based Access Control**: Database models and basic superuser enforcement.
- **Threat Intel IOC Tracking**: Local database management of indicators (IPs, hashes).
- **Malware Sample Management**: Tracking for reverse-engineering artifact metadata.
- **Dashboard**: Aggregate metric displays and recent activity feeds.
- **Organizational Grouping**: Foundational multi-tenant models.

### 🗺️ Planned Roadmap
- **AI Investigation Workspace (Architecture Ready)**: UI is complete; backend currently returns mocked reasoning steps pending LLM integration.
- **SOAR Playbook Management**: Drag-and-drop playbook design UI is complete; execution engine planned.
- **Threat Hunting Workspace**: Query saving exists; advanced telemetry search engine planned.
- **External Integrations**: VirusTotal, AlienVault OTX, and Sandbox API synchronization.
- **Executive Reporting**: Scheduled PDF report generation.

---

## 📸 Screenshots

> Click any image to view full size.

| Dashboard | Alerts |
|-----------|--------|
| ![Dashboard](screenshots/dashboard.png) | ![Alerts](screenshots/alerts.png) |
| Threat metrics with alert severity breakdown and analyst workload distribution | Active alert queue with MITRE ATT&CK technique tagging and one-click case promotion |

| Cases | Threat Intelligence |
|-------|-------------------|
| ![Cases](screenshots/cases.png) | ![Threat Intel](screenshots/threat-intelligence.png) |
| Full incident timeline with artifact linking, analyst notes, and severity tracking | IOC management and indicator reputation tracking |

| Malware Analysis | Threat Hunting |
|-----------------|----------------|
| ![Malware](screenshots/malware-analysis.png) | ![Hunting](screenshots/threat-hunting.png) |
| Malware artifact tracking with SHA256 tracking and case linkage | Threat hunting query workspace |

| SOAR Automation |
|----------------|
| ![SOAR](screenshots/soar.png) |
| Drag-and-drop playbook builder interface |

## 🎥 Demo Walkthrough

[![Watch Demo](screenshots/dashboard.png)](https://loom.com/REPLACE_WITH_YOUR_LINK)

> Walkthrough — Docker boot → Alert ingestion → Case creation

*Record free at [loom.com](https://loom.com)*

---

## 🏗️ System Architecture

Sentrix is designed as a high-performance web application utilizing a microservices-inspired monolithic architecture.

```mermaid
graph TD
    Client[Web Browser] -->|HTTPS| Proxy[Nginx / Traefik]
    
    subgraph "Frontend Tier"
        Proxy --> UI[Next.js 14 App Router]
        UI --> ReactQuery[TanStack Query]
        UI --> Tailwind[TailwindCSS]
    end
    
    subgraph "Backend Tier"
        UI -->|REST API| API[FastAPI Gateway]
        API --> Auth[Auth Middleware]
        Auth --> Controllers[Routers]
        Controllers --> Services[Service Layer]
        Services --> Repos[Repository Layer]
    end
    
    subgraph "Data Tier"
        Repos --> PG[(PostgreSQL 16 + SQLAlchemy 2.0)]
        Repos --> Redis[(Redis 7)]
    end
    
    style Client fill:#1e293b,color:#fff,stroke:#334155
    style UI fill:#0ea5e9,color:#fff,stroke:#0284c7
    style API fill:#10b981,color:#fff,stroke:#059669
    style PG fill:#3b82f6,color:#fff,stroke:#2563eb
    style Redis fill:#ef4444,color:#dc2626
```

### Request Lifecycle

```mermaid
sequenceDiagram
    participant Client
    participant FastAPI
    participant Auth
    participant Service
    participant Database
    
    Client->>FastAPI: HTTP Request (e.g., GET /api/v1/alerts)
    FastAPI->>Auth: Verify JWT Token
    Auth-->>FastAPI: User Context
    FastAPI->>Service: Call Business Logic
    Service->>Database: Execute Async SQL Query
    Database-->>Service: Return ORM Models
    Service-->>FastAPI: Return Pydantic Schemas
    FastAPI-->>Client: JSON Response
```

---

## 🔄 SOC Investigation Workflow

The primary goal of Sentrix is to streamline the incident response pipeline.

```mermaid
flowchart TD
    A[Alert Ingestion] --> B{Triage}
    
    B -->|False Positive| C[Close Alert]
    B -->|True Positive| D[Assign Analyst]
    
    D --> E[Create Investigation Case]
    
    E --> F[Threat Intel Lookup]
    F --> G[Threat Hunting]
    G --> H[Malware Analysis]
    
    H --> I[Assign SOAR Playbook]
    I --> J[Containment & Remediation]
    
    J --> K[Executive Reporting]
    K --> L[Close Case]
    
    style I fill:#8b5cf6,color:#fff,stroke:#7c3aed
    style A fill:#3b82f6,color:#fff,stroke:#2563eb
    style L fill:#10b981,color:#fff,stroke:#059669
```

---

## 🛠️ Technology Stack

| Domain | Technology | Description |
| :--- | :--- | :--- |
| **Frontend Framework** | Next.js (App Router) | High-performance React framework. |
| **Styling & UI** | TailwindCSS + Lucide Icons | Utility-first CSS and modern SVGs. |
| **State & Fetching** | TanStack React Query | Advanced caching, deduplication, and polling. |
| **Backend API** | FastAPI (Python 3.11) | Ultra-fast, async Python web framework. |
| **Database (Relational)** | PostgreSQL 16 + SQLAlchemy 2.0 | Primary data store with fully async ORM. |
| **Caching & Auth** | Redis 7 | JWT blacklisting and ephemeral state. |
| **Containerization** | Docker + Docker Compose | Isolated, reproducible deployment environments. |

---

## 📁 Project Structure

```text
SentriX/
├── backend/               # FastAPI backend application
│   ├── app/               # Main application logic (API, Models, Services)
│   ├── alembic/           # Database migrations
│   ├── scripts/           # DB seeding and utility scripts
│   └── tests/             # Backend unit and integration tests
├── frontend/              # Next.js frontend application
│   ├── app/               # Next.js App Router pages
│   ├── components/        # Reusable UI components
│   └── lib/               # Utility functions and API clients
├── screenshots/           # UI screenshots for README
├── assets/                # Logos and banners
├── .github/               # Issue templates and PR guidelines
└── docker-compose.yml     # Local orchestration
```

---

## 🗄️ Database Schema

Built on strict SQLAlchemy 2.0 ORM models with `UUID` primary keys, soft-deletion capabilities, and robust cascading relationships.

```mermaid
erDiagram
    USERS ||--o{ CASES : "assigns"
    USERS {
        uuid id PK
        string email
        string hashed_password
        string role
        boolean is_active
    }
    
    CASES ||--o{ ALERTS : "contains"
    CASES {
        uuid id PK
        string title
        string status
        string severity
        uuid assignee_id FK
    }
    
    ALERTS ||--o{ ASSETS : "impacts"
    ALERTS {
        uuid id PK
        string rule_name
        string severity
        jsonb payload
    }
    
    MALWARE_SAMPLES ||--o{ CASES : "links_to"
    MALWARE_SAMPLES {
        uuid id PK
        string sha256
        string verdict
        int threat_score
    }
```

---

## 🔌 API Documentation

Sentrix provides beautiful Swagger/OpenAPI documentation auto-generated by FastAPI.

- **Swagger UI**: `/docs` (e.g. `http://localhost:8000/docs`)
- **ReDoc**: `/redoc` (e.g. `http://localhost:8000/redoc`)

Example Request (Create Alert):
```bash
curl -X POST "http://localhost:8000/api/v1/alerts" \
     -H "Authorization: Bearer <your_token>" \
     -H "Content-Type: application/json" \
     -d '{"rule_name": "Suspicious Login", "severity": "HIGH", "status": "OPEN"}'
```

---

## 🚀 Quick Start

### 1-Click Startup (Docker)

Get the entire Sentrix platform running locally:

```bash
# 1. Clone the repository
git clone https://github.com/alive-xd/SentriX.git
cd SentriX

# 2. Copy the environment variables
cp backend/.env.example backend/.env

# 3. Start the infrastructure (Postgres, Redis, Backend)
docker compose up -d

# 4. In a separate terminal, install and start the frontend
cd frontend
npm install
npm run dev
```

Navigate to [http://localhost:3000](http://localhost:3000) and login with the default seeded credentials:
- **Email**: `admin@stark.com`
- **Password**: `password123`

---

## ⚙️ Installation

For bare-metal local installation without Docker:
1. Ensure **PostgreSQL 16** and **Redis 7** are running on your host.
2. Setup a Python 3.11 virtual environment for the backend and install `backend/requirements.txt`.
3. Run migrations via `alembic upgrade head`.
4. Run the backend via `uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4`.
5. Build the frontend via `npm run build` and start via `npm run start`.

---

## 🔑 Environment Variables

Crucial environment variables defined in `backend/.env`:

| Variable | Description |
| :--- | :--- |
| `DATABASE_URL` | PostgreSQL Async connection string (`postgresql+asyncpg://`) |
| `REDIS_URL` | Redis connection string (`redis://`) |
| `SECRET_KEY` | 256-bit secret for JWT Signing. **Must be rotated in production.** |

---

## 🌱 Database Seeding

To populate the database with realistic alerts, cases, malware samples, and threat intelligence for testing:

```bash
docker compose exec backend python -m scripts.seed_database
```
This automatically inserts exactly 485 alerts, 120 cases, 300 threat indicators, 150 assets, and 1000 audit logs into the database.

---

## 🔐 Security Features

- **JWT (JSON Web Tokens)**: Secure tokens with Redis-backed refresh token rotation and logout blocklisting.
- **Password Hashing**: Industry-standard `bcrypt` hashing via `passlib`.
- **Foundational Role-Based Access Control**: Database structures preventing privilege escalation.
- **SQL Injection Protection**: Pure reliance on SQLAlchemy ORM parameterized queries.
- **Input Validation**: Pydantic v2 schemas rigorously sanitize all incoming API payloads.

---

## 🛡️ Architecture & Threat Model

- **Trust Boundaries**: The API Gateway (FastAPI) acts as the sole entry point to the data tier. All internal inter-service communication (PostgreSQL, Redis) is assumed secure behind the internal Docker bridge network.
- **Data at Rest**: Sensitive Analyst passwords are cryptographically secured.
- **Data in Transit**: Production deployments should terminate TLS at a Reverse Proxy.

---

## 🧪 Testing

Sentrix has a foundational test suite to ensure API health and basic authentication enforcement.

Run the unit tests locally:
```bash
cd backend
pytest -v
```

---

## 📖 Documentation

The entire platform documentation is self-contained within this README to ensure a single source of truth for all architectural, deployment, and operational procedures. 

---

## ❓ FAQ

**Q: Can I use Sentrix to replace my SIEM?**
A: No, Sentrix is designed as a SOAR and Case Management workspace intended to sit *on top* of a SIEM.

**Q: Is there a paid Enterprise version?**
A: No. Sentrix is 100% open-source under the MIT license.

---

## 🤝 Contributing

We welcome contributions from the global cybersecurity and open-source software communities! 

Please read our [Contributing Guide](CONTRIBUTING.md) to get started with branching rules, PR templates, and issue tracking.

---

## 📅 Changelog

See [CHANGELOG.md](CHANGELOG.md) for detailed version history.

---

## 🙏 Acknowledgements

Special thanks to the open-source projects that made this possible:
- **FastAPI** by Tiangolo
- **Next.js** by Vercel
- **PostgreSQL** community

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
