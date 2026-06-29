from typing import Any, Sequence
from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.case import Case, CaseStatus
from app.models.alert import Alert, AlertStatus, AlertSeverity
from app.models.asset import Asset, AssetStatus
from app.models.detection import DetectionRule, RuleStatus
from app.models.threat_intel import ThreatIndicator


class DashboardService:
    async def get_summary(self, db: AsyncSession) -> dict[str, Any]:
        """Top-level KPI metrics for the SOC overview panel."""
        open_cases = (await db.execute(
            select(func.count()).where(Case.status == CaseStatus.OPEN)
        )).scalar_one()

        in_progress_cases = (await db.execute(
            select(func.count()).where(Case.status == CaseStatus.IN_PROGRESS)
        )).scalar_one()

        new_alerts = (await db.execute(
            select(func.count()).where(Alert.status == AlertStatus.NEW)
        )).scalar_one()

        critical_alerts = (await db.execute(
            select(func.count()).where(
                Alert.severity == AlertSeverity.CRITICAL,
                Alert.status == AlertStatus.NEW,
            )
        )).scalar_one()

        total_assets = (await db.execute(
            select(func.count()).select_from(Asset)
        )).scalar_one()

        active_assets = (await db.execute(
            select(func.count()).where(Asset.status == AssetStatus.ACTIVE)
        )).scalar_one()

        active_rules = (await db.execute(
            select(func.count()).where(DetectionRule.status == RuleStatus.ACTIVE)
        )).scalar_one()

        active_iocs = (await db.execute(
            select(func.count()).where(ThreatIndicator.is_active)
        )).scalar_one()

        return {
            "cases": {
                "open": open_cases,
                "in_progress": in_progress_cases,
                "total_active": open_cases + in_progress_cases,
            },
            "alerts": {
                "new": new_alerts,
                "critical": critical_alerts,
            },
            "assets": {
                "total": total_assets,
                "active": active_assets,
            },
            "detections": {
                "active_rules": active_rules,
            },
            "threat_intel": {
                "active_iocs": active_iocs,
            },
        }

    async def get_severity_breakdown(self, db: AsyncSession) -> dict[str, Any]:
        """Case and alert counts grouped by severity."""
        case_severity = (await db.execute(
            select(Case.severity, func.count().label("count"))
            .group_by(Case.severity)
        )).all()

        alert_severity = (await db.execute(
            select(Alert.severity, func.count().label("count"))
            .where(Alert.status == AlertStatus.NEW)
            .group_by(Alert.severity)
        )).all()

        return {
            "cases_by_severity": {row.severity.value: row.count for row in case_severity},
            "alerts_by_severity": {row.severity.value: row.count for row in alert_severity},
        }

    async def get_recent_alerts(self, db: AsyncSession, limit: int = 10) -> Sequence[Alert]:
        """Most recent N alerts for the activity feed."""
        result = await db.execute(
            select(Alert)
            .order_by(Alert.created_at.desc())
            .limit(limit)
        )
        return result.scalars().all()

    async def get_activity_feed(self, db: AsyncSession, limit: int = 20) -> Sequence[Case]:
        """Recent cases ordered by last update for the activity feed."""
        result = await db.execute(
            select(Case)
            .order_by(Case.updated_at.desc())
            .limit(limit)
        )
        return result.scalars().all()


dashboard_service = DashboardService()
