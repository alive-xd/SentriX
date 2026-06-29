<div align="center">
  <img src="assets/banner.png" alt="Sentrix Banner" width="100%" />

  <br />
  <br />

  <h1>🛡️ Sentrix Platform</h1>
  <p><strong>The Next-Generation, AI-Powered Enterprise Security Operations Center (SOC)</strong></p>

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
    <strong>A high-performance, open-source security intelligence platform built for modern blue teams.</strong>
  </p>
</div>

---

## 🌟 Overview

**Sentrix** is a feature-complete, enterprise-grade Security Operations Center (SOC) platform designed to aggregate, analyze, and act upon cyber threats in real-time. 

Built with modern architectural patterns (Next.js App Router, FastAPI, PostgreSQL, and Redis), Sentrix empowers cybersecurity professionals, incident responders, and security analysts to drastically reduce Mean Time To Respond (MTTR) by centralizing Alert Management, Threat Intelligence, Malware Analysis, and SOAR (Security Orchestration, Automation, and Response) pipelines into a single, intuitive interface.

---

## ✨ Key Features

- ✅ **Alert Management**: Real-time aggregation of security alerts across the network.
- ✅ **Case Management**: Collaborate on complex incidents with timelines and artifact linking.
- ✅ **Threat Intelligence**: Built-in support for multiple OSINT feeds.
- ✅ **Malware Analysis**: Automated sandboxing integration and reverse-engineering artifact tracking.
- ✅ **Threat Hunting**: Fast, indexed querying over massive security telemetry logs.
- ✅ **SOAR Automation**: Drag-and-drop playbook creation for automated incident response.
- ✅ **AI Investigation Assistant**: LLM-backed reasoning engine to triage false positives.
- ✅ **Reporting**: Beautifully formatted, compliance-ready executive reports.

---

## 📸 Screenshots

*Explore the platform through our highly-polished UI.*

<details>
<summary><b>View Gallery (Click to expand)</b></summary>
<br/>

| Dashboard | Alerts |
| :---: | :---: |
| <img src="screenshots/dashboard.png" alt="Dashboard" width="100%" /> | <img src="screenshots/alerts.png" alt="Alerts" width="100%" /> |

| Cases | Threat Intelligence |
| :---: | :---: |
| <img src="screenshots/cases.png" alt="Cases" width="100%" /> | <img src="screenshots/threat-intelligence.png" alt="Threat Intelligence" width="100%" /> |

| Malware Analysis | Threat Hunting |
| :---: | :---: |
| <img src="screenshots/malware-analysis.png" alt="Malware Analysis" width="100%" /> | <img src="screenshots/threat-hunting.png" alt="Threat Hunting" width="100%" /> |

| SOAR Automation | Reporting |
| :---: | :---: |
| <img src="screenshots/soar.png" alt="SOAR Automation" width="100%" /> | <img src="screenshots/reports.png" alt="Reports" width="100%" /> |

</details>

---

## 🏗️ System Architecture

Sentrix is designed as a modern, high-performance web application utilizing a microservices-inspired monolithic architecture. It separates the high-performance UI tier from the deeply asynchronous processing tier.

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
        Repos --> Qdrant[(Qdrant Vector DB)]
    end
    
    style Client fill:#1e293b,color:#fff,stroke:#334155
    style UI fill:#0ea5e9,color:#fff,stroke:#0284c7
    style API fill:#10b981,color:#fff,stroke:#059669
    style PG fill:#3b82f6,color:#fff,stroke:#2563eb
    style Redis fill:#ef4444,color:#fff,stroke:#dc2626
    style Qdrant fill:#f43f5e,color:#fff,stroke:#e11d48
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

## 🔄 SOC Workflow (Incident Lifecycle)

The primary goal of Sentrix is to streamline the incident response pipeline, converting raw telemetry and alerts into actionable intelligence and automated responses.

```mermaid
flowchart TD
    A[Alert Ingestion] --> B{Triage}
    
    B -->|False Positive| C[Close Alert]
    B -->|True Positive| D[Assign Analyst]
    
    D --> E[Create Investigation Case]
    
    E --> F[Threat Intel Lookup]
    F --> G[Threat Hunting]
    G --> H[Malware Analysis]
    
    H --> I[Execute SOAR Playbook]
    I --> J[Containment & Remediation]
    
    J --> K[Executive Reporting]
    K --> L[Close Case]
    
    style I fill:#8b5cf6,color:#fff,stroke:#7c3aed
    style A fill:#3b82f6,color:#fff,stroke:#2563eb
    style L fill:#10b981,color:#fff,stroke:#059669
```

---

## 🗄️ Database Schema (ERD)

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

## 📚 API Documentation

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

## 🧪 Final Acceptance & E2E Testing

Sentrix has undergone rigorous End-to-End (E2E) testing and validation to guarantee production readiness before release.

### 1. Environment Verification
- **Docker & Services**: Verified `docker-compose up -d` boots PostgreSQL, Redis, Qdrant, and FastAPI seamlessly.
- **Data Seeding**: The `seed_database.py` script successfully populates all ORM entities (Alerts, Cases, Threat Intel, SOAR Playbooks).

### 2. Authentication & RBAC
- Confirmed full JWT lifecycle (`login` -> `token refresh` -> `blocklist logout`).
- Validated Role-Based Access Control (RBAC) ensuring non-admin users cannot mutate global settings.

### 3. Comprehensive Module Verification
All primary CRUD modules were rigorously tested via API and UI:
- **Dashboard**: KPI metrics and temporal distribution charts render perfectly.
- **Alerts**: Read, filter, acknowledge, and dismiss functionality.
- **Cases**: Full investigation lifecycle from creation to closure, linking artifacts.
- **Malware**: Sandbox verdicts and IOC extraction visualization.
- **Threat Intel**: Dynamic querying and caching of OSINT feeds.
- **Threat Hunting**: Vector and SQL-based querying of raw log data.
- **SOAR**: Execution tracing of automated playbooks.

### 4. E2E SOC Workflow Audit
We simulated a real-world breach scenario ("Suspicious Powershell Execution"):
1. The **Alert** was ingested and triaged.
2. Promoted to an **Investigation Case**.
3. **Malware** sample linked to the case and analyzed.
4. **Threat Hunting** utilized to find lateral movement.
5. **SOAR Playbook** triggered to isolate the compromised asset.
6. A **Report** was generated and the case successfully closed.

**Outcome**: Sentrix passed all acceptance criteria with zero blocking defects.

---

## 🚀 Quick Start (Installation)

### Prerequisites
- [Docker](https://docs.docker.com/get-docker/) & Docker Compose
- [Node.js](https://nodejs.org/en/) 18+ (for local frontend dev)
- [Python](https://www.python.org/) 3.11+ (for local backend dev)

### 1-Click Startup (Docker)

Get the entire Sentrix platform running locally in under 60 seconds:

```bash
# 1. Clone the repository
git clone https://github.com/alive-xd/SentriX.git
cd SentriX

# 2. Copy the environment variables
cp backend/.env.example backend/.env

# 3. Start the infrastructure (Postgres, Redis, Qdrant, Backend)
docker compose up -d

# 4. In a separate terminal, install and start the frontend
cd frontend
npm install
npm run dev
```

Navigate to [http://localhost:3000](http://localhost:3000) and login with the default seeded credentials:
- **Email**: `admin@sentrix.local`
- **Password**: `admin`

---

## 🤝 Contributing

We welcome contributions from the global cybersecurity and open-source software communities! 

Whether it's adding a new OSINT integration, fixing a UI bug, or optimizing a database query, please read our [Contributing Guide](CONTRIBUTING.md) to get started.

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

<div align="center">
  <i>Engineered with precision for the modern SOC.</i>
</div>
