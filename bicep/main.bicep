// Devopstrio AIOps Incident Predictor - Master Bicep Deployment
targetScope = 'subscription'

param location string = 'uksouth'
param env string = 'prod'
param prefix string = 'aiops'

// 1. Core Resource Group
resource rg 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: 'rg-${prefix}-${env}'
  location: location
}

// 2. Hub/Spoke Networking
module network './modules/network.bicep' = {
  scope: rg
  name: 'networkDeploy'
  params: {
    location: location
    vnetName: 'vnet-${prefix}-${env}'
  }
}

// 3. PostgreSQL Database (State)
module data './modules/data.bicep' = {
  scope: rg
  name: 'dataDeploy'
  params: {
    location: location
    serverName: 'psql-${prefix}-${env}'
    subnetId: network.outputs.dbSubnetId
  }
}

// 4. Monitoring & Telemetry (Log Analytics / App Insights)
module monitoring './modules/monitoring.bicep' = {
  scope: rg
  name: 'monitoringDeploy'
  params: {
    location: location
    workspaceName: 'law-${prefix}-${env}'
  }
}

output platformUrl string = 'https://aiops.devopstrio.co.uk'
