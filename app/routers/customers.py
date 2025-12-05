from fastapi import HTTPException, status, APIRouter
from sqlmodel import select

from models import CustomerCreate, CustomerUpdate, Customer
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
    return { "detail": "Customer deleted" }


@router.patch("/customer/{id}", response_model=Customer, status_code=status.HTTP_201_CREATED, tags=["customers"])
async def update_customer_by_id(id: int, data: CustomerUpdate, session: SessionDependency):
    customer = session.get(Customer, id)
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found")
    data_dict = data.model_dump(exclude_unset = True)
    customer.sqlmodel_update(data_dict)
    session.add(customer)
    session.commit()
    session.refresh(customer)
    return customer