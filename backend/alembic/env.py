import asyncio
from logging.config import fileConfig
from sqlalchemy import pool
from sqlalchemy.engine import Connection
from sqlalchemy.ext.asyncio import async_engine_from_config
from alembic import context

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from app.db.base_class import Base

# Import ALL models so Alembic picks them up for autogenerate
from app.models.organization import Organization
from app.models.role import Role
from app.models.user import User
from app.models.api_key import ApiKey
from app.models.case import Case
from app.models.alert import Alert
from app.models.case_activity import CaseComment, CaseTimeline
from app.models.investigation import Investigation
from app.models.asset import Asset, AssetVulnerability
from app.models.threat_intel import ThreatIndicator, ThreatActor, ThreatFeed
from app.models.malware_sample import MalwareSample
from app.models.detection import DetectionRule, RuleTest
from app.models.playbook import Playbook
from app.models.integration import Integration
from app.models.report import Report
from app.models.audit_log import AuditLog
from app.models.notification import Notification
from app.models.ai_audit_log import AIAuditLog

# Alembic Config object
config = context.config

# Logging setup
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

# Metadata for autogenerate
target_metadata = Base.metadata


def get_url():
    return settings.sqlalchemy_database_uri


def run_migrations_offline() -> None:
    """Run migrations in 'offline' mode."""
    url = get_url()
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()


def do_run_migrations(connection: Connection) -> None:
    context.configure(connection=connection, target_metadata=target_metadata)
    with context.begin_transaction():
        context.run_migrations()


async def run_async_migrations() -> None:
    configuration = config.get_section(config.config_ini_section, {})
    configuration["sqlalchemy.url"] = get_url()
    connectable = async_engine_from_config(
        configuration,
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )
    async with connectable.connect() as connection:
        await connection.run_sync(do_run_migrations)
    await connectable.dispose()


def run_migrations_online() -> None:
    asyncio.run(run_async_migrations())


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
