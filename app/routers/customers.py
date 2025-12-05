from fastapi import HTTPException, status, APIRouter, Query
from sqlmodel import select

from models import CustomerCreate, CustomerUpdate, Customer, Plan, CustomerPlan, StatusEnum
from db import SessionDependency

router = APIRouter()

db_customers: list[Customer] = []


@router.post("/customers", response_model=Customer, tags=["customers"])
async def create_customer(data: CustomerCreate, session: SessionDependency):
    customer = Customer.model_validate(data.model_dump())

    # save in database
    session.add(customer)
    session.commit()
    session.refresh(customer)

    """
    In local memory
    customer.id = len(db_customers)
    db_customers.append(customer)
    """
    return customer


@router.get("/customers", response_model=list[Customer], tags=["customers"])
async def get_customers(session: SessionDependency):
    """
    In local memory
    return db_customers
    """
    return session.exec(select(Customer)).all()


@router.get("/customer/{id}", response_model=Customer, tags=["customers"])
async def get_customer_by_id(id: int, session: SessionDependency):
    """
    In local memory
    customer = next((c for c in db_customers if c.id == id), None)
    """
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    return customer


@router.delete("/customer/{id}", tags=["customers"])
async def remove_customer_by_id(id: int, session: SessionDependency):
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    session.delete(customer)
    session.commit()
    return {"detail": "Customer deleted"}


@router.patch("/customer/{id}", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=["customers"])
async def update_customer_by_id(id: int, data: CustomerUpdate, session: SessionDependency):
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    data_dict = data.model_dump(exclude_unset=True)
    customer.sqlmodel_update(data_dict)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer


@router.post("/customers/{customer_id}/plans/{plan_id}", response_model=CustomerPlan,
             status_code=status.HTTP_201_CREATED, tags=["customers"])
async def subscribe_customer_to_plan(customer_id: int, plan_id: int, session: SessionDependency,
                                     plan_status: StatusEnum = Query()):
    customer_bd = session.get(Customer, customer_id)
    plan_bd = session.get(Plan, plan_id)

    if not customer_bd or not plan_bd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer or plan not found")

    customer_plan_db = CustomerPlan(plan_id=plan_bd.id, customer_id=customer_bd.id, status=plan_status)
    session.add(customer_plan_db)
    session.commit()
    session.refresh(customer_plan_db)
    return customer_plan_db


@router.get("/customers/{customer_id}/plans", response_model=list[Plan], tags=["customers"])
async def get_customer_subscriptions(customer_id: int, session: SessionDependency, plan_status: StatusEnum = Query()):
    customer_bd = session.get(Customer, customer_id)

    if not customer_bd:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")

    query = (select(CustomerPlan)
             .where(CustomerPlan.customer_id == customer_bd.id)
             .where(CustomerPlan.status == plan_status)
             )
    plans = session.exec(query).all()
    return plans
