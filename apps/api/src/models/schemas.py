from sqlalchemy import Column, String, Float, Integer, ForeignKey, DateTime, JSON, Boolean, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
import uuid
import datetime
from ..db.database import Base

# SQLAlchemy ORM Models mirroring database schema

class Tenant(Base):
    __tablename__ = "tenants"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True)
    subscription_tier = Column(String, default="Enterprise")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class CMDBAsset(Base):
    __tablename__ = "cmdb_assets"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    asset_name = Column(String, nullable=False, index=True)
    asset_type = Column(String, nullable=False)
    tags = Column(JSON, default={})
    business_criticality = Column(Integer, default=3)
    environment = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    asset_id = Column(UUID(as_uuid=True), ForeignKey("cmdb_assets.id"))
    alert_name = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    status = Column(String, default="open")
    raw_payload = Column(JSON, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    title = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    state = Column(String, default="investigating")
    root_cause_asset_id = Column(UUID(as_uuid=True), ForeignKey("cmdb_assets.id"))
    associated_alerts = Column(JSON, default=[])
    itsm_ticket_id = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved_at = Column(DateTime)

class Prediction(Base):
    __tablename__ = "predictions"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"))
    asset_id = Column(UUID(as_uuid=True), ForeignKey("cmdb_assets.id"))
    prediction_type = Column(String, nullable=False)
    probability = Column(Float, nullable=False)
    time_to_impact_minutes = Column(Integer, nullable=False)
    mitigation_strategy = Column(Text)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Pydantic Schemas for API Requests/Responses (kept in same file for brevity, though commonly separate)
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime as dt

class PredictionOut(BaseModel):
    id: uuid.UUID
    asset_id: Optional[uuid.UUID]
    prediction_type: str
    probability: float
    time_to_impact_minutes: int
    mitigation_strategy: Optional[str]
    created_at: dt

    class Config:
        orm_mode = True

class IncidentCreate(BaseModel):
    title: str
    severity: str
    associated_alerts: List[str]

class IncidentOut(BaseModel):
    id: uuid.UUID
    title: str
    severity: str
    state: str
    itsm_ticket_id: Optional[str]
    created_at: dt

    class Config:
        orm_mode = True
