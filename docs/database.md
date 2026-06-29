# Database Schema

Sentrix uses PostgreSQL 16 as its primary relational data store, managed via SQLAlchemy 2.0 (async).

## Entity Relationship Diagram (ERD)

```mermaid
erDiagram
    USERS ||--o{ CASES : "assigns"
    USERS {
        uuid id PK
        string email
        string hashed_password
        string full_name
        string role
        boolean is_active
        datetime created_at
    }
    
    CASES ||--o{ ALERTS : "contains"
    CASES {
        uuid id PK
        string title
        string description
        string status
        string severity
        uuid assignee_id FK
        datetime created_at
    }
    
    ALERTS ||--o{ ASSETS : "impacts"
    ALERTS {
        uuid id PK
        string rule_name
        string severity
        string status
        jsonb payload
        uuid asset_id FK
    }
    
    MALWARE_SAMPLES ||--o{ CASES : "links_to"
    MALWARE_SAMPLES {
        uuid id PK
        string file_name
        string sha256
        string verdict
        int threat_score
        string severity
    }
    
    ASSETS {
        uuid id PK
        string hostname
        string ip_address
        string os_type
        string risk_level
    }
    
    PLAYBOOKS {
        uuid id PK
        string name
        string description
        boolean is_active
        jsonb steps
    }
```

## Schema Details

### Base Models
All tables inherit from a declarative base that includes:
- `UUIDMixin`: Uses PostgreSQL UUID generation (`gen_random_uuid()`).
- `TimestampMixin`: Automatically handles `created_at` and `updated_at`.
- `SoftDeleteMixin`: Provides a `deleted_at` column to prevent accidental data destruction.

### Migrations
Database schema changes are tracked using **Alembic**.

To generate a new migration:
```bash
alembic revision --autogenerate -m "added new table"
```

To apply migrations:
```bash
alembic upgrade head
```
