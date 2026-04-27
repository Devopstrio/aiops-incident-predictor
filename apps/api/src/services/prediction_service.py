import logging
from sqlalchemy.orm import Session
from ..models.schemas import Prediction

logger = logging.getLogger(__name__)

class PredictionService:
    @staticmethod
    def get_active_predictions(db: Session, limit: int = 50):
        """
        Retrieves active failure predictions that have a high probability.
        """
        try:
            return db.query(Prediction).filter(Prediction.probability > 0.70).order_by(Prediction.created_at.desc()).limit(limit).all()
        except Exception as e:
            logger.error(f"Error fetching predictions: {str(e)}")
            raise

    @staticmethod
    def get_prediction_by_id(db: Session, prediction_id: str):
        """
        Retrieves a single predictive alert detail.
        """
        try:
            return db.query(Prediction).filter(Prediction.id == prediction_id).first()
        except Exception as e:
            logger.error(f"Error fetching prediction by ID {prediction_id}: {str(e)}")
            raise
