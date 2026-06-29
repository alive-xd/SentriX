from typing import Any, List, Dict
from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import or_

from app.db.session import get_db
from app.models.case import Case
from app.models.alert import Alert
from app.models.asset import Asset
from app.models.playbook import Playbook
from app.models.user import User

from sqlalchemy.future import select

router = APIRouter()

@router.get("/")
async def global_search(
    q: str,
    db: AsyncSession = Depends(get_db),
) -> Dict[str, List[Any]]:
    if not q:
        return {"cases": [], "alerts": [], "assets": [], "playbooks": [], "users": []}

    search_term = f"%{q}%"

    # Cases
    stmt_cases = select(Case).filter(or_(Case.title.ilike(search_term), Case.description.ilike(search_term))).limit(5)
    cases_result = await db.execute(stmt_cases)
    cases = cases_result.scalars().all()

    # Alerts
    stmt_alerts = select(Alert).filter(or_(Alert.title.ilike(search_term), Alert.description.ilike(search_term))).limit(5)
    alerts_result = await db.execute(stmt_alerts)
    alerts = alerts_result.scalars().all()

    # Assets
    stmt_assets = select(Asset).filter(or_(Asset.hostname.ilike(search_term), Asset.ip_address.ilike(search_term))).limit(5)
    assets_result = await db.execute(stmt_assets)
    assets = assets_result.scalars().all()

    # Playbooks
    stmt_playbooks = select(Playbook).filter(or_(Playbook.name.ilike(search_term), Playbook.description.ilike(search_term))).limit(5)
    playbooks_result = await db.execute(stmt_playbooks)
    playbooks = playbooks_result.scalars().all()

    # Users
    stmt_users = select(User).filter(or_(User.full_name.ilike(search_term), User.email.ilike(search_term))).limit(5)
    users_result = await db.execute(stmt_users)
    users = users_result.scalars().all()

    return {
        "cases": cases,
        "alerts": alerts,
        "assets": assets,
        "playbooks": playbooks,
        "users": users
    }
