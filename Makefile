.PHONY: up down build logs shell test migrate db-revision psql gen-secret lint format

# ─── Docker ───────────────────────────────────────────────────────────────────
up:
	docker-compose up -d

down:
	docker-compose down

build:
	docker-compose build --no-cache

logs:
	docker-compose logs -f backend

shell:
	docker-compose exec backend bash

# ─── Database ─────────────────────────────────────────────────────────────────
# Usage: make db-revision m="describe your migration"
db-revision:
	docker-compose exec backend alembic revision --autogenerate -m "$(m)"

migrate:
	docker-compose exec backend alembic upgrade head

rollback:
	docker-compose exec backend alembic downgrade -1

psql:
	docker-compose exec postgres psql -U sentrix -d sentrix_db

# ─── Testing ──────────────────────────────────────────────────────────────────
test:
	docker-compose exec backend pytest -v --tb=short

test-cov:
	docker-compose exec backend pytest --cov=app --cov-report=term-missing

# ─── Code Quality ─────────────────────────────────────────────────────────────
lint:
	docker-compose exec backend ruff check app

format:
	docker-compose exec backend black app

# ─── Utilities ────────────────────────────────────────────────────────────────
gen-secret:
	@python -c "import secrets; print(secrets.token_hex(32))"
