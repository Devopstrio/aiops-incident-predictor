from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from ..db.database import get_db
from ..services.prediction_service import PredictionService
from ..models.schemas import PredictionOut

router = APIRouter(prefix="/api/v1/predictions", tags=["Predictions"])

@router.get("/", response_model=List[PredictionOut])
def list_predictions(db: Session = Depends(get_db)):
    """
    Returns a list of predictive alerts and anomaly forecasts.
    """
    return PredictionService.get_active_predictions(db)

@router.get("/{prediction_id}", response_model=PredictionOut)
def get_prediction(prediction_id: str, db: Session = Depends(get_db)):
    """
    Returns the details of a specific predictive alert.
    """
    prediction = PredictionService.get_prediction_by_id(db, prediction_id)
    if not prediction:
        raise HTTPException(status_code=404, detail="Prediction not found")
    return prediction
