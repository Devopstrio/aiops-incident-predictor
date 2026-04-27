import logging
import time
import hashlib

# AIOps: Correlation Engine
# Purpose: Suppress noise, cluster alerts topographically, and extract single Root Cause Incidents.

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger("AIOps-CorrelationEngine")

class AlertCorrelator:
    def __init__(self):
        self.active_alert_cache = {}

    def deduplicate(self, raw_alert: dict) -> bool:
        """Returns True if the alert is new, False if it is a duplicate."""
        # Simple signature based on source and metric
        sig = f"{raw_alert['source']}_{raw_alert['metric']}"
        sig_hash = hashlib.md5(sig.encode()).hexdigest()
        
        if sig_hash in self.active_alert_cache:
            return False
            
        self.active_alert_cache[sig_hash] = time.time()
        return True

    def cluster_events(self, active_alerts: list) -> list:
        """Groups alerts based on CMDB topology (e.g., all alerts from DB cluster X)."""
        logger.info(f"Clustering {len(active_alerts)} raw active alerts...")
        # Simulating clustering logic: if multiple alerts, they form one incident
        if len(active_alerts) > 1:
            return [{
                "incident_title": "Database Degradation Cluster",
                "severity": "Critical",
                "suppressed_alerts_count": len(active_alerts) - 1,
                "root_cause_candidate": active_alerts[0] # Simplification
            }]
        return []

def main_loop():
    correlator = AlertCorrelator()
    while True:
        logger.info("Listening for raw alerts from Ingestion Engine...")
        time.sleep(10)
        
        # Simulate processing an alert storm
        alerts = [
            {"source": "aks-db-pod-1", "metric": "cpu_high", "val": 99},
            {"source": "aks-db-pod-2", "metric": "cpu_high", "val": 98},
            {"source": "aks-db-pod-1", "metric": "conn_drop", "val": 1}
        ]
        
        unique_alerts = [a for a in alerts if correlator.deduplicate(a)]
        logger.info(f"Deduplication complete: {len(alerts)} raw -> {len(unique_alerts)} unique")
        
        incidents = correlator.cluster_events(unique_alerts)
        for inc in incidents:
            logger.error(f"🔥 CORRELATED INCIDENT DETECTED: {inc['incident_title']} (Suppressed {inc['suppressed_alerts_count']} redundant alerts)")

if __name__ == "__main__":
    logger.info("Starting Correlation Engine Worker")
    main_loop()
