from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..services.incident_service import IncidentService
from ..models.schemas import IncidentOut, IncidentCreate

router = APIRouter(prefix="/api/v1/incidents", tags=["Incidents"])

@router.get("/", response_model=List[IncidentOut])
def list_incidents(db: Session = Depends(get_db)):
    """
    Returns a list of all correlated incidents.
    """
    return IncidentService.get_incidents(db)

@router.post("/create", response_model=IncidentOut)
def create_incident(incident: IncidentCreate, db: Session = Depends(get_db)):
    """
    Trigger the creation of an incident through the correlation pipeline.
    """
    # Assuming a default dummy tenant for demonstration
    tenant_id = "00000000-0000-0000-0000-000000000000"
    try:
        return IncidentService.create_incident(db, incident, tenant_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
