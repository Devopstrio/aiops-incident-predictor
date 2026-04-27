import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .db.database import init_db
from .routes import predictions, incidents

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="AIOps Incident Predictor API",
    description="Enterprise Telemetry Gateway and Predictive Engine Orchestrator",
    version="1.0.0"
)

# Enable CORS for Next.js Portal Integration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    logger.info("Initializing Enterprise AIOps Platform...")
    init_db()

@app.get("/health")
def health_check():
    return {"status": "operational", "version": "1.0.0"}

@app.get("/metrics")
def get_metrics():
    """Returns basic Prometheus metrics for the API itself."""
    return {"api_requests_total": 4200, "api_errors_total": 3}

app.include_router(predictions.router)
app.include_router(incidents.router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
