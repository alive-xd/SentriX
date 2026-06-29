from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
import asyncio
from datetime import datetime

from app.db.session import get_db
from app.services.report_service import report_service
from app.schemas.report import Report, ReportCreate, ReportUpdate

router = APIRouter()

class ReportListResponse(BaseModel):
    items: List[Report]
    total: int
    skip: int
    limit: int

@router.get("/", response_model=ReportListResponse)
async def get_reports(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    items, total = await report_service.get_multi(
        db, skip=skip, limit=limit
    )
    return {"items": items, "total": total, "skip": skip, "limit": limit}

@router.post("/", response_model=Report)
async def create_report(
    *,
    db: AsyncSession = Depends(get_db),
    obj_in: ReportCreate,
) -> Any:
    return await report_service.create(db, obj_in=obj_in)

@router.patch("/{id}", response_model=Report)
async def update_report(
    *,
    db: AsyncSession = Depends(get_db),
    id: str,
    obj_in: ReportUpdate,
) -> Any:
    report = await report_service.get(db, id=id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    return await report_service.update(db, db_obj=report, obj_in=obj_in)

@router.delete("/{id}")
async def delete_report(
    *,
    db: AsyncSession = Depends(get_db),
    id: str,
) -> Any:
    await report_service.delete(db, id=id)
    return {"status": "success"}

@router.post("/{id}/generate")
async def generate_report(
    *,
    db: AsyncSession = Depends(get_db),
    id: str,
) -> Any:
    report = await report_service.get(db, id=id)
    if not report:
        raise HTTPException(status_code=404, detail="Report not found")
    
    # We do the work here or in a background task
    # For now we'll just wait simulating a report generation
    await report_service.generate_report(db, id=id)
    return {"status": "success"}
