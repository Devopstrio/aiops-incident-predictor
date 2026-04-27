-- Devopstrio AIOps Incident Predictor
-- Enterprise Database Schema definition
-- Target: PostgreSQL 14+

CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tenants Table for Multi-Tenancy Support
CREATE TABLE IF NOT EXISTS tenants (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(255) UNIQUE NOT NULL,
    subscription_tier VARCHAR(50) DEFAULT 'Enterprise',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Users & Roles for RBAC
CREATE TABLE IF NOT EXISTS roles (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name VARCHAR(50) UNIQUE NOT NULL,
    permissions JSONB NOT NULL DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS users (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    role_id UUID REFERENCES roles(id),
    email VARCHAR(255) UNIQUE NOT NULL,
    full_name VARCHAR(255) NOT NULL,
    is_active BOOLEAN DEFAULT true,
    last_login TIMESTAMP WITH TIME ZONE,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Configuration Management Database (CMDB) Assets
CREATE TABLE IF NOT EXISTS cmdb_assets (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    asset_name VARCHAR(255) NOT NULL,
    asset_type VARCHAR(100) NOT NULL, -- e.g., 'VM', 'K8s_Cluster', 'Database'
    tags JSONB DEFAULT '{}',
    business_criticality INT DEFAULT 3, -- 1=Low, 5=Mission Critical
    environment VARCHAR(50) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Service Dependencies Graph Edges
CREATE TABLE IF NOT EXISTS service_dependencies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_asset_id UUID REFERENCES cmdb_assets(id) ON DELETE CASCADE,
    target_asset_id UUID REFERENCES cmdb_assets(id) ON DELETE CASCADE,
    dependency_type VARCHAR(100) NOT NULL, -- 'calls', 'hosted_on', 'reads_from'
    UNIQUE(source_asset_id, target_asset_id)
);

-- Telemetry Logs & Metrics (Hot Tier)
CREATE TABLE IF NOT EXISTS telemetry_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    asset_id UUID REFERENCES cmdb_assets(id) ON DELETE SET NULL,
    log_level VARCHAR(50),
    message TEXT,
    event_timestamp TIMESTAMP WITH TIME ZONE NOT NULL,
    metadata JSONB DEFAULT '{}'
);

CREATE TABLE IF NOT EXISTS telemetry_metrics (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    asset_id UUID REFERENCES cmdb_assets(id) ON DELETE SET NULL,
    metric_name VARCHAR(255) NOT NULL,
    metric_value FLOAT NOT NULL,
    event_timestamp TIMESTAMP WITH TIME ZONE NOT NULL
);

-- Alerts (Raw signals from monitoring tools)
CREATE TABLE IF NOT EXISTS alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    asset_id UUID REFERENCES cmdb_assets(id) ON DELETE SET NULL,
    alert_name VARCHAR(255) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    status VARCHAR(50) DEFAULT 'open', -- open, acknowledged, suppressed, resolved
    raw_payload JSONB NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Correlated Incidents
CREATE TABLE IF NOT EXISTS incidents (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    title VARCHAR(255) NOT NULL,
    severity VARCHAR(50) NOT NULL,
    state VARCHAR(50) DEFAULT 'investigating', -- investigating, identified, monitoring, resolved, closed
    root_cause_asset_id UUID REFERENCES cmdb_assets(id) ON DELETE SET NULL,
    associated_alerts JSONB DEFAULT '[]', -- Array of Alert IDs
    itsm_ticket_id VARCHAR(100),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    resolved_at TIMESTAMP WITH TIME ZONE
);

-- ML Predictions
CREATE TABLE IF NOT EXISTS predictions (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    asset_id UUID REFERENCES cmdb_assets(id) ON DELETE SET NULL,
    prediction_type VARCHAR(100) NOT NULL, -- 'capacity_exhaustion', 'latency_spike'
    probability FLOAT NOT NULL,
    time_to_impact_minutes INT NOT NULL,
    mitigation_strategy TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Automated Remediation Runs
CREATE TABLE IF NOT EXISTS remediation_runs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    incident_id UUID REFERENCES incidents(id) ON DELETE CASCADE,
    workflow_name VARCHAR(255) NOT NULL,
    status VARCHAR(50) DEFAULT 'running', -- running, success, failed
    execution_logs TEXT,
    started_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP WITH TIME ZONE
);

-- SLA Policies
CREATE TABLE IF NOT EXISTS sla_policies (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    policy_name VARCHAR(255) NOT NULL,
    target_metric VARCHAR(100) NOT NULL,
    threshold FLOAT NOT NULL,
    operator VARCHAR(10) NOT NULL, -- '>', '<', '=='
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Audit Trailing
CREATE TABLE IF NOT EXISTS audit_logs (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    user_id UUID REFERENCES users(id) ON DELETE SET NULL,
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    action VARCHAR(255) NOT NULL,
    resource_type VARCHAR(100),
    resource_id UUID,
    changes JSONB DEFAULT '{}',
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Reporting Cache
CREATE TABLE IF NOT EXISTS reports (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    report_type VARCHAR(100) NOT NULL,
    report_data JSONB NOT NULL,
    generated_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for standard access paths
CREATE INDEX idx_telemetry_metrics_ts ON telemetry_metrics(event_timestamp);
CREATE INDEX idx_alerts_status ON alerts(status);
CREATE INDEX idx_incidents_state ON incidents(state);
CREATE INDEX idx_predictions_asset ON predictions(asset_id);
