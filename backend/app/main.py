from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logging import setup_logging
from app.core.exceptions import AppException, app_exception_handler, global_exception_handler
from app.db.redis import init_redis_pool, close_redis_pool
from app.api.v1 import health, auth, users, alerts, cases, investigations, assets, threat_intel, dashboard, detections, knowledge, soar, malware, hunts, reports, ai, search

logger = setup_logging()

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup actions
    logger.info("Starting up Sentrix Backend...")
    await init_redis_pool()
    logger.info("Redis pool initialized.")
    yield
    # Shutdown actions
    logger.info("Shutting down Sentrix Backend...")
    await close_redis_pool()
    logger.info("Redis pool closed.")

app = FastAPI(
    title=settings.PROJECT_NAME,
    description="AI-powered Security Operations Center platform (Foundation Level)",
    version="1.0.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# Exception Handlers
app.add_exception_handler(AppException, app_exception_handler)
app.add_exception_handler(Exception, global_exception_handler)

# CORS — restrict to frontend origin in production
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ─── API Routers (Foundation Only) ───────────────────────────────────────────
API = settings.API_V1_STR

app.include_router(health.router, tags=["Health"])
app.include_router(auth.router, prefix=f"{API}/auth", tags=["Authentication"])
app.include_router(users.router, prefix=f"{API}/users", tags=["Users"])
app.include_router(alerts.router, prefix=f"{API}/alerts", tags=["Alerts"])
app.include_router(cases.router, prefix=f"{API}/cases", tags=["Cases"])
app.include_router(investigations.router, prefix=f"{API}/investigations", tags=["Investigations"])
app.include_router(assets.router, prefix=f"{API}/assets", tags=["Assets"])
app.include_router(threat_intel.router, prefix=f"{API}/threat-intel", tags=["Threat Intelligence"])
app.include_router(dashboard.router, prefix=f"{API}/dashboard", tags=["Dashboard"])
app.include_router(detections.router, prefix=f"{API}/detections", tags=["Detections"])
app.include_router(search.router, prefix=f"{API}/search", tags=["Search"])
app.include_router(knowledge.router, prefix=f"{API}/knowledge", tags=["Knowledge Base"])
app.include_router(soar.router, prefix=f"{API}/soar", tags=["SOAR"])
app.include_router(malware.router, prefix=f"{API}/malware", tags=["Malware"])
app.include_router(hunts.router, prefix=f"{API}/threat-hunting", tags=["Threat Hunting"])
app.include_router(reports.router, prefix=f"{API}/reports", tags=["Reports"])
app.include_router(ai.router, prefix=f"{API}/ai", tags=["AI"])


