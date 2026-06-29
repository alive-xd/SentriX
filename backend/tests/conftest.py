import pytest
from unittest.mock import AsyncMock, MagicMock
from fastapi.testclient import TestClient
from app.main import app
from app.db.redis import get_redis
from app.db.session import get_db

@pytest.fixture(autouse=True)
def override_dependencies():
    async def override_get_redis():
        mock = AsyncMock()
        yield mock

    async def override_get_db():
        mock = AsyncMock()
        yield mock

    app.dependency_overrides[get_redis] = override_get_redis
    app.dependency_overrides[get_db] = override_get_db
    yield
    app.dependency_overrides.clear()
