from fastapi import APIRouter
from models import Plan
from sqlmodel import select

from db import SessionDependency

router = APIRouter()


@router.post("/plans", tags=["plans"])
async def create_plan(data: Plan, session: SessionDependency):
    plan_bd = Plan.model_validate(data.model_dump())
    session.add(plan_bd)
    session.commit()
    session.refresh(plan_bd)
    return plan_bd


@router.get("/plans", response_model=list[Plan], tags=["plans"])
async def get_plans(session: SessionDependency):
    plans = session.exec(select(Plan)).all()
    return plans
