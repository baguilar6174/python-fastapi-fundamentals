import time

from fastapi import FastAPI, Request, Depends, HTTPException, status
from datetime import datetime
import zoneinfo
from fastapi.security import HTTPBasicCredentials, HTTPBasic
from typing import Annotated

from db import create_all_tables
from .routers import customers, transactions, invoices, plans

app = FastAPI(lifespan=create_all_tables)
app.include_router(customers.router)
app.include_router(transactions.router)
app.include_router(invoices.router)
app.include_router(plans.router)


@app.middleware("http")
async def log_request_time(request: Request, call_next):
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    print(f"{request.url} completed in {process_time:.4f} seconds")
    return response


@app.get("/")
async def root():
    return {"message": "Hello World"}


security = HTTPBasic()


@app.get("/admin")
async def admin_endpoint(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    if credentials.username == "admin" and credentials.password == "password":
        return {"message": f"Hello {credentials.username}!"}
    else:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)


timezones = {
    "CO": "America/Bogota",
    "MX": "America/Mexico_City",
    "PE": "America/Lima",
    "AZ": "America/Sao_Paulo",
}


@app.get("/time/{iso_code}")
async def get_time_by_iso_code(iso_code: str):
    iso = iso_code.upper()
    timezone = timezones.get(iso)
    tz = zoneinfo.ZoneInfo(timezone)
    return {"time": datetime.now(tz)}
