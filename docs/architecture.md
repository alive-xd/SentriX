# Sentrix Architecture

Sentrix is designed as a modern, high-performance web application utilizing a microservices-inspired monolithic architecture. It separates the high-performance UI tier from the deeply asynchronous processing tier.

## System Diagram

```mermaid
graph TD
    Client[Web Browser] -->|HTTPS| Proxy[Nginx / Traefik]
    
    subgraph "Frontend Tier"
        Proxy --> UI[Next.js App Router]
        UI --> ReactQuery[TanStack Query]
    end
    
    subgraph "Backend Tier"
        UI -->|REST API| API[FastAPI Gateway]
        API --> Auth[Auth Middleware]
        Auth --> Controllers[Routers]
        Controllers --> Services[Service Layer]
        Services --> Repos[Repository Layer]
    end
    
    subgraph "Data Tier"
        Repos --> PG[(PostgreSQL 16)]
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

## Core Components

### 1. Frontend (Next.js)
The frontend uses **Next.js 14+** leveraging the App Router. 
- **Styling**: TailwindCSS provides a utility-first styling approach.
- **State Management**: TanStack React Query handles server state, caching, and background polling.
- **Components**: Modular, reusable React components under `/components/ui`.

### 2. Backend (FastAPI)
The backend is powered by **FastAPI (Python 3.11+)**.
- **Asynchronous**: Fully asynchronous endpoints utilizing `async/await`.
- **Validation**: Strict input validation using Pydantic schemas.
- **Dependency Injection**: Heavy use of FastAPI's dependency injection system for database sessions and authentication.

### 3. Database (PostgreSQL & SQLAlchemy)
- **PostgreSQL 16**: Primary relational database.
- **SQLAlchemy 2.0**: Asynchronous ORM (`asyncpg`).
- **Alembic**: Database schema migrations.

### 4. Caching & Message Broker (Redis)
- **Redis 7**: Used for caching API responses, blacklisting JWT tokens, and rate-limiting.

### 5. AI & Vector Search (Qdrant)
- **Qdrant**: High-performance vector database used for semantic search over threat intelligence and AI reasoning.

## Request Lifecycle

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
