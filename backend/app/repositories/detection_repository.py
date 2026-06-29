import uuid
from typing import Optional, List, Tuple
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession
from app.models.detection import DetectionRule, RuleTest, RuleStatus, RuleSeverity, RuleType
from app.schemas.detection import (
    DetectionRuleCreate, DetectionRuleUpdate,
    RuleTestCreate, DetectionRuleStats,
)


class DetectionRepository:
    async def get_by_id(self, db: AsyncSession, rule_id: uuid.UUID) -> Optional[DetectionRule]:
        result = await db.execute(select(DetectionRule).where(DetectionRule.id == rule_id))
        return result.scalars().first()

    async def get_multi(
        self,
        db: AsyncSession,
        *,
        skip: int = 0,
        limit: int = 50,
        status: Optional[RuleStatus] = None,
        severity: Optional[RuleSeverity] = None,
        rule_type: Optional[RuleType] = None,
        search: Optional[str] = None,
    ) -> Tuple[List[DetectionRule], int]:
        query = select(DetectionRule)
        filters = []
        if status:
            filters.append(DetectionRule.status == status)
        if severity:
            filters.append(DetectionRule.severity == severity)
        if rule_type:
            filters.append(DetectionRule.rule_type == rule_type)
        if search:
            filters.append(DetectionRule.name.ilike(f"%{search}%"))
        if filters:
            query = query.where(and_(*filters))

        count_result = await db.execute(select(func.count()).select_from(query.subquery()))
        total = count_result.scalar_one()

        query = query.order_by(DetectionRule.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(query)
        return result.scalars().all(), total

    async def create(
        self, db: AsyncSession, obj_in: DetectionRuleCreate, created_by_id: uuid.UUID
    ) -> DetectionRule:
        db_obj = DetectionRule(**obj_in.model_dump(), created_by_id=created_by_id)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update(
        self, db: AsyncSession, db_obj: DetectionRule,
        obj_in: DetectionRuleUpdate, modified_by_id: uuid.UUID
    ) -> DetectionRule:
        for field, value in obj_in.model_dump(exclude_unset=True).items():
            setattr(db_obj, field, value)
        db_obj.last_modified_by_id = modified_by_id
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def delete(self, db: AsyncSession, db_obj: DetectionRule) -> None:
        await db.delete(db_obj)
        await db.commit()

    async def activate(self, db: AsyncSession, db_obj: DetectionRule, user_id: uuid.UUID) -> DetectionRule:
        db_obj.is_enabled = True
        db_obj.status = RuleStatus.ACTIVE
        db_obj.last_modified_by_id = user_id
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def deactivate(self, db: AsyncSession, db_obj: DetectionRule, user_id: uuid.UUID) -> DetectionRule:
        db_obj.is_enabled = False
        db_obj.status = RuleStatus.INACTIVE
        db_obj.last_modified_by_id = user_id
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def add_test_run(
        self, db: AsyncSession, rule_id: uuid.UUID, ran_by_id: uuid.UUID, obj_in: RuleTestCreate
    ) -> RuleTest:
        test = RuleTest(rule_id=rule_id, ran_by_id=ran_by_id, **obj_in.model_dump())
        db.add(test)
        await db.commit()
        await db.refresh(test)
        return test

    async def get_stats(self, db: AsyncSession) -> DetectionRuleStats:
        total = (await db.execute(select(func.count()).select_from(DetectionRule))).scalar_one()
        active = (await db.execute(select(func.count()).where(DetectionRule.status == RuleStatus.ACTIVE))).scalar_one()
        testing = (await db.execute(select(func.count()).where(DetectionRule.status == RuleStatus.TESTING))).scalar_one()
        inactive = (await db.execute(select(func.count()).where(DetectionRule.status == RuleStatus.INACTIVE))).scalar_one()
        total_hits = (await db.execute(select(func.sum(DetectionRule.hit_count)))).scalar_one() or 0
        return DetectionRuleStats(
            total=total, active=active, testing=testing,
            inactive=inactive, total_hits=total_hits,
        )


detection_repo = DetectionRepository()
