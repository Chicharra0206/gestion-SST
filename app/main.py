import os
import sys
from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from .config import settings
from .database import Base, engine, get_db
from .models import Company
from .schemas import CompanyBulkUpsert, CompanyListResponse, CompanyPayload, CompanyResponse, HealthResponse


def get_frontend_path() -> str:
    if getattr(sys, 'frozen', False):
        base = os.path.dirname(sys.executable)
    else:
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base, "dashboard-hqse.html")


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(title="Dashboard HQSE API", version="1.0.0", lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origin_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/app")
def serve_frontend():
    path = get_frontend_path()
    return FileResponse(path, media_type="text/html")


@app.get("/api/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/api/companies", response_model=CompanyListResponse)
def list_companies(db: Session = Depends(get_db)) -> CompanyListResponse:
    companies = db.query(Company).order_by(Company.name.asc()).all()
    return CompanyListResponse(companies=companies)


@app.put("/api/companies/bulk", response_model=CompanyListResponse)
def bulk_upsert_companies(payload: CompanyBulkUpsert, db: Session = Depends(get_db)) -> CompanyListResponse:
    existing = {company.id: company for company in db.query(Company).all()}

    for item in payload.companies:
        row = existing.get(item.id)
        if row:
            row.name = item.name
            row.data = item.data
        else:
            db.add(Company(id=item.id, name=item.name, data=item.data))

    payload_ids = {company.id for company in payload.companies}
    for company_id, row in existing.items():
        if company_id not in payload_ids:
            db.delete(row)

    db.commit()
    companies = db.query(Company).order_by(Company.name.asc()).all()
    return CompanyListResponse(companies=companies)


@app.post("/api/companies", response_model=CompanyResponse)
def create_company(payload: CompanyPayload, db: Session = Depends(get_db)) -> CompanyResponse:
    row = Company(id=payload.id, name=payload.name, data=payload.data)
    db.add(row)
    db.commit()
    db.refresh(row)
    return row
