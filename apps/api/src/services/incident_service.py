import logging
from sqlalchemy.orm import Session
from ..models.schemas import Incident, IncidentCreate

logger = logging.getLogger(__name__)

class IncidentService:
    @staticmethod
    def get_incidents(db: Session, limit: int = 100):
        """
        Retrieves recent incidents sorted by creation date.
        """
        try:
            return db.query(Incident).order_by(Incident.created_at.desc()).limit(limit).all()
        except Exception as e:
            logger.error(f"Error fetching incidents: {str(e)}")
            raise

    @staticmethod
    def create_incident(db: Session, incident: IncidentCreate, tenant_id: str):
        """
        Manually or Programmatically creates a new incident.
        """
        try:
            new_incident = Incident(
                tenant_id=tenant_id,
                title=incident.title,
                severity=incident.severity,
                associated_alerts=incident.associated_alerts,
                state="investigating"
            )
            db.add(new_incident)
            db.commit()
            db.refresh(new_incident)
            logger.info(f"✅ Incident Created: {new_incident.id}")
            return new_incident
        except Exception as e:
            db.rollback()
            logger.error(f"❌ Error creating incident: {str(e)}")
            raise
