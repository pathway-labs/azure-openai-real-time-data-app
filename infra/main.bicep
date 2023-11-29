targetScope = 'subscription'

@minLength(1)
@maxLength(64)
@description('Name of the the environment which is used to generate a short unique hash used in all resources.')
param environmentName string

@minLength(1)
@description('Primary location for all resources')
param location string

param appServicePlanName string = ''
param backendServiceName string = ''
param resourceGroupName string = ''

param applicationInsightsDashboardName string = ''
param applicationInsightsName string = ''
param logAnalyticsName string = ''

@allowed(['azure', 'openai'])
param openAiHost string // Set in main.parameters.json

param openAiServiceName string = ''
param openAiResourceGroupName string = ''
@description('Location for the OpenAI resource group')
@allowed(['canadaeast', 'eastus', 'eastus2', 'francecentral', 'switzerlandnorth', 'uksouth', 'japaneast', 'northcentralus', 'australiaeast', 'swedencentral'])
@metadata({
  azd: {
    type: 'location'
  }
})
param openAiResourceGroupLocation string

param openAiSkuName string = 'S0'

param chatGptDeploymentName string // Set in main.parameters.json
param chatGptDeploymentCapacity int = 30
param chatGptModelName string = (openAiHost == 'azure') ? 'gpt-35-turbo' : 'gpt-3.5-turbo'
param chatGptModelVersion string = '0613'
param embeddingDeploymentName string // Set in main.parameters.json
param embeddingDeploymentCapacity int = 30
param embeddingModelName string = 'text-embedding-ada-002'
param openAiApiKey string // Set in main.parameters.json

param frontendStreamlitName string = 'frontend'
param frontendStreamlitImageName string = ''

param backendApiName string = 'backend'
param backendApiImageName string = ''

param eventHubsNamespaceConnectionString string // Set in main.parameters.json

@description('Use Application Insights for monitoring and performance tracing')
param useApplicationInsights bool = false

var abbrs = loadJsonContent('abbreviations.json')
var resourceToken = toLower(uniqueString(subscription().id, environmentName, location))
var tags = { 'azd-env-name': environmentName }

// Organize resources in a resource group
resource resourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' = {
  name: !empty(resourceGroupName) ? resourceGroupName : '${abbrs.resourcesResourceGroups}${environmentName}'
  location: location
  tags: tags
}

resource openAiResourceGroup 'Microsoft.Resources/resourceGroups@2021-04-01' existing = if (!empty(openAiResourceGroupName)) {
  name: !empty(openAiResourceGroupName) ? openAiResourceGroupName : resourceGroup.name
}

// Monitor application with Azure Monitor
module monitoring './core/monitor/monitoring.bicep' = {
  name: 'monitoring'
  scope: resourceGroup
  params: {
    location: location
    tags: tags
    logAnalyticsName: '${abbrs.operationalInsightsWorkspaces}${resourceToken}'
    applicationInsightsName: useApplicationInsights ? '${abbrs.insightsComponents}${resourceToken}' : ''
  }
}

// Event Hubs
module eventHubs './core/data/event-hubs.bicep' = {
  name: 'event-hubs'
  scope: resourceGroup
  params: {
    location: location
  }
}

// Container apps host (including container registry)
module containerApps './core/host/container-apps.bicep' = {
  name: 'container-apps'
  scope: resourceGroup
  params: {
    name: 'containerapps'
    containerAppsEnvironmentName: '${abbrs.appManagedEnvironments}${resourceToken}'
    containerRegistryName: '${abbrs.containerRegistryRegistries}${resourceToken}'
    location: location
    tags: tags
    logAnalyticsWorkspaceName: monitoring.outputs.logAnalyticsWorkspaceName
  }
}

// The backend API
module backendApi './core/host/container-app.bicep' = {
  name: 'backend-api'
  scope: resourceGroup
  params: {
    name: !empty(backendApiName) ? backendApiName : '${abbrs.appContainerApps}api-${resourceToken}'
    location: location
    tags: union(tags, { 'azd-service-name': 'backend' })
    containerAppsEnvironmentName: containerApps.outputs.environmentName
    containerRegistryName: containerApps.outputs.registryName
    managedIdentity: true
    containerCpuCoreCount: '1.0'
    containerMemory: '2.0Gi'
    secrets: useApplicationInsights ? [
      {
        name: 'appinsights-cs'
        value: monitoring.outputs.applicationInsightsConnectionString
      }
    ] : []
    env: concat([
      {
        name: 'AZURE_OPENAI_CHATGPT_DEPLOYMENT'
        value: chatGptDeploymentName
      }
      {
        name: 'AZURE_OPENAI_CHATGPT_MODEL'
        value: chatGptModelName
      }
      {
        name: 'AZURE_OPENAI_EMB_DEPLOYMENT'
        value: embeddingDeploymentName
      }
      {
        name: 'AZURE_OPENAI_EMBEDDING_MODEL'
        value: embeddingModelName
      }
      {
        name: 'AZURE_OPENAI_API_KEY'
        value: openAiApiKey
      }
      {
        name: 'AZURE_OPENAI_SERVICE'
        value: openAi.outputs.name
      }
      {
        name: 'EVENT_HUBS_NAMESPACE_CONNECTION_STRING'
        value: eventHubsNamespaceConnectionString
      }
    ], useApplicationInsights ? [{
      name: 'APPLICATIONINSIGHTS_CONNECTION_STRING'
      secretRef: 'appinsights-cs'
    }] : [])
    imageName: !empty(backendApiImageName) ? backendApiImageName : 'python:3.11'
    targetPort: 8080
  }
}


// The frontend UI
module frontendStreamlit './core/host/container-app.bicep' = {
  name: 'frontend-streamlit'
  scope: resourceGroup
  params: {
    name: !empty(frontendStreamlitName) ? frontendStreamlitName : '${abbrs.appContainerApps}ui-${resourceToken}'
    location: location
    tags: union(tags, { 'azd-service-name': 'frontend' })
    containerAppsEnvironmentName: containerApps.outputs.environmentName
    containerRegistryName: containerApps.outputs.registryName
    managedIdentity: true
    containerCpuCoreCount: '1.0'
    containerMemory: '2.0Gi'
    env: concat([
      {
        name: 'BACKEND_API_URI'
        value: backendApi.outputs.uri
      }
    ])
    imageName: !empty(frontendStreamlitImageName) ? frontendStreamlitImageName : 'python:3.11'
    targetPort: 8501
  }
}


module openAi 'core/ai/cognitiveservices.bicep' = if (openAiHost == 'azure') {
  name: 'openai'
  scope: openAiResourceGroup
  params: {
    name: !empty(openAiServiceName) ? openAiServiceName : '${abbrs.cognitiveServicesAccounts}${resourceToken}'
    location: openAiResourceGroupLocation
    tags: tags
    sku: {
      name: openAiSkuName
    }
    deployments: [
      {
        name: chatGptDeploymentName
        model: {
          format: 'OpenAI'
          name: chatGptModelName
          version: chatGptModelVersion
        }
        sku: {
          name: 'Standard'
          capacity: chatGptDeploymentCapacity
        }
      }
      {
        name: embeddingDeploymentName
        model: {
          format: 'OpenAI'
          name: embeddingModelName
          version: '2'
        }
        capacity: embeddingDeploymentCapacity
      }
    ]
  }
}

output AZURE_LOCATION string = location
output AZURE_TENANT_ID string = tenant().tenantId
output AZURE_RESOURCE_GROUP string = resourceGroup.name

output AZURE_CONTAINER_REGISTRY_ENDPOINT string = containerApps.outputs.registryLoginServer
output AZURE_CONTAINER_REGISTRY_NAME string = containerApps.outputs.registryName

// Shared by all OpenAI deployments
output OPENAI_HOST string = openAiHost
output AZURE_OPENAI_EMB_MODEL_NAME string = embeddingModelName
output AZURE_OPENAI_CHATGPT_MODEL string = chatGptModelName
// Specific to Azure OpenAI
output AZURE_OPENAI_SERVICE string = openAi.outputs.name
output AZURE_OPENAI_RESOURCE_GROUP string = (openAiHost == 'azure') ? openAiResourceGroup.name : ''
output AZURE_OPENAI_CHATGPT_DEPLOYMENT string = (openAiHost == 'azure') ? chatGptDeploymentName : ''
output AZURE_OPENAI_EMB_DEPLOYMENT string = (openAiHost == 'azure') ? embeddingDeploymentName : ''

output BACKEND_API_URI string = backendApi.outputs.uri

output EVENT_HUBS_NAMESPACE_CONNECTION_STRING string = eventHubsNamespaceConnectionString

