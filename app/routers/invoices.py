from fastapi import APIRouter
from models import Invoice

router = APIRouter()

@router.post("/invoices", tags=["invoices"])
async def create_invoice(data: Invoice):
    return data