# Data streaming for real-time enterprise AI apps

This repository demonstrates how to build real-time generative AI applications using [Azure Event Hubs](https://learn.microsoft.com/en-us/azure/event-hubs/azure-event-hubs-kafka-overview) + [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) + [Pathway](https://pathway.com/)’s [LLM App](https://github.com/pathwaycom/llm-app)+[Streamlit](https://streamlit.io/).

- [Data streaming for real-time enterprise AI apps](#data-streaming-for-real-time-enterprise-ai-apps)
  - [Motivation](#motivation)
  - [Example scenario: Customer support and sentiment analysis dashboard](#example-scenario-customer-support-and-sentiment-analysis-dashboard)
    - [Background](#background)
    - [Implementation](#implementation)
    - [Overview of the Azure services the sample project uses](#overview-of-the-azure-services-the-sample-project-uses)
    - [Azure infrastructure with the main components](#azure-infrastructure-with-the-main-components)
    - [One click running app demo](#one-click-running-app-demo)
  - [Setup the project](#setup-the-project)
    - [Prerequisites](#prerequisites)
    - [Open in GitHub Codespaces](#open-in-github-codespaces)
    - [Open in Dev Container](#open-in-dev-container)
    - [Local environment](#local-environment)
    - [Run the project locally](#run-the-project-locally)
    - [Deploy from scratch](#deploy-from-scratch)
    - [Deploy with existing Azure resources](#deploy-with-existing-azure-resources)
      - [Existing Azure resource group](#existing-azure-resource-group)
      - [Existing Azure OpenAI resource](#existing-azure-openai-resource)

## Motivation

Real-time AI app needs real-time data to respond with the most up-to-date information to user queries or perform quick actions autonomously. To reduce cost and infrastructural complexity, you can build a real-time data pipeline with Azure Event Hubs, Pathway, and Azure OpenAI. This integrated system leverages the strengths of Pathway for robust data processing, LLMs like GPT for advanced text analytics, and Streamlit for user-friendly data visualization. 

This combination empowers businesses to build and deploy enterprise AI applications that provide the freshest contextual visual data. 

## Example scenario: Customer support and sentiment analysis dashboard

### Background

For example, a multinational corporation wants to improve its customer support by analyzing customer feedback and inquiries in real-time. They aim to understand common issues, track customer sentiment, and identify areas for improvement in their products and services. To achieve this, they need a system that can process large data streams, analyze text for insights, and present these insights in an accessible way.

### Implementation

1. **Azure Event Hubs & Kafka: Real-Time Data Streaming and Processing**
    
    Azure Event Hubs collects real-time data from various sources, such as customer feedback forms, support chat logs, and social media mentions. This data is then streamed into a Kafka cluster for further processing.
    
2. **Large Language Models (LLMs) like GPT from Azure OpenAI: Text Analysis and Sentiment Detection**
    
    The text data from Kafka is fed into an LLM for natural language processing using Pathway. This model performs sentiment analysis, key phrase extraction, and feedback categorization (e.g., identifying common issues or topics).
    
3. **Pathway to enable real-time data pipeline**
    
    Pathway gains access to the data streams from Azure Event Hubs, it preprocesses, transforms, or joins them and the [LLM App](https://github.com/pathwaycom/llm-app) helps to bring real-time context to the AI App with real-time vector indexing, semantic search, and retrieval capabilities. The text content of the events will be sent to Azure OpenAI embedding APIs via the LLM App to compute the embeddings and vector representations will be indexed. 
    
    Using the LLM app, the company can gain deep insights from unstructured text data, understanding the sentiment and nuances of customer feedback.
    
4. **Streamlit: Interactive Dashboard for Visualization**
    
    Streamlit is used to create an interactive web dashboard that visualizes the insights derived from customer feedback. This dashboard can show real-time metrics such as overall sentiment trends, and common topics in customer feedback, and even alert the team to emerging issues (See [example](https://github.com/pathwaycom/llm-app/tree/main/examples/pipelines/drive_alert) implementation of alerting to enhance this project).

### Overview of the Azure services the sample project uses

| Service | Purpose |
| --- | --- |
| [Azure AI Services](https://azure.microsoft.com/en-us/products/ai-services?activetab=pivot:azureopenaiservicetab) | To use Azure OpenAI GPT model and embeddings. |
| [Azure Event Hubs](https://azure.microsoft.com/en-us/products/event-hubs) | To stream real-time events from various data sources. |
| [Azure Container Apps](https://learn.microsoft.com/azure/container-apps/?WT.mc_id=javascript-0000-cxa) | Hosts our containerized applications (backend and frontend) with features like auto-scaling and load balancing. |
| [Azure Container Registry](https://learn.microsoft.com/azure/container-registry/?WT.mc_id=javascript-0000-cxa) | Stores our Docker container images in a managed, private registry. |
| [Azure Log Analytics](https://learn.microsoft.com/azure/log-analytics/?WT.mc_id=javascript-0000-cxa) | Collects and analyzes telemetry and logs for insights into application performance and diagnostics. |
| [Azure Monitor](https://learn.microsoft.com/azure/azure-monitor/?WT.mc_id=javascript-0000-cxa) | Provides comprehensive monitoring of our applications, infrastructure, and network. |

### Azure infrastructure with the main components

![Azure Infrastructure Diagram](/assets/azure-infra-architecture.png)

### One click running app demo

Follow the link to see the running UI app in Azure:

[Customer support and sentiment analysis dashboard](https://frontend.greensmoke-e214d1a7.francecentral.azurecontainerapps.io/)

It builds a real-time dashboard based on an example prompt we provided to analyze the data.

## Setup the project

To set up the project you need to follow the below steps:

1. You have an Azure account with the required settings specified in the [Prerequisites](#prerequisites) section.
2. Choose one of these environments to open the project:
    1. [GitHub Codespaces](#open-in-github-codespaces).
    2. [VS Code Dev Containers](#open-in-dev-container).
    3. [Local environment](#local-environment).
3. Follow the [deploy from scratch](#deploy-from-scratch) or [deploy with existing Azure resources](#deploy-with-existing-azure-resources) guide.

### Prerequisites

**Azure account requirements:** To run and deploy the example project, you'll need:

- **Azure account**. If you're new to Azure, [get an Azure account for free](https://azure.microsoft.com/free/cognitive-search/) and you'll get some free Azure credits to get started.
- **Azure subscription with access enabled for the Azure OpenAI service**. You can apply for access to Azure OpenAI by completing the form at https://aka.ms/oai/access.

### Open in GitHub Codespaces

Follow these steps to open the project in a Codespace:

1. Click here to open in GitHub Codespaces

[![Open in GitHub Codespaces](https://img.shields.io/static/v1?style=for-the-badge&label=GitHub+Codespaces&message=Open&color=lightgrey&logo=github)](https://codespaces.new/pathway-labs/azure-openai-real-time-data-app)

2. Next -> [deploy from scratch](#deploy-from-scratch) or [deploy with existing Azure resources](#deploy-with-existing-azure-resources).

### Open in Dev Container

1. Click here to open in Dev Container

[![Open in Dev Container](https://img.shields.io/static/v1?style=for-the-badge&label=Dev+Container&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/pathway-labs/azure-openai-real-time-data-app)

2. Next -> [deploy from scratch](#deploy-from-scratch) or [deploy with existing Azure resources](#deploy-with-existing-azure-resources).

### Local environment

First, install the required tools:

- [Azure Developer CLI](https://aka.ms/azure-dev/install)
- [Python 3.9, 3.10, or 3.11](https://www.python.org/downloads/)
    - **Important**: Ensure you can run `python --version` from the console. On Ubuntu, you might need to run `sudo apt install python-is-python3` to link `python` to `python3`.
- [Git](https://git-scm.com/downloads)
- [Install WSL](https://learn.microsoft.com/en-us/windows/wsl/install) - For Windows users only.
- [Powershell 7+ (pwsh)](https://github.com/powershell/powershell) - For Windows users only.
    - **Important**: Ensure you can run `pwsh.exe` from a PowerShell terminal. If this fails, you likely need to upgrade PowerShell.

Then bring down the project code:

1. Open a terminal.
2. Run `azd auth login` and log in using your Azure account credentials.
3. Run `azd init -t https://github.com/pathway-labs/azure-openai-real-time-data-app`. This command will initialize a git repository and you do not need to clone this repository.
4. When the project starts, the system prompts you to enter a new environment name: `AZURE_ENV_NAME`. Read more [manage environment variables](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/manage-environment-variables). For example, any name like: *pathway* and outputs for infrastructure provisioning are automatically stored as environment variables in an `.env` file, located under `.azure/pathway/.env` in the project folder.
5. Then, follow the [deploying from scratch](#deploy-from-scratch) guide.

### Run the project locally

1. Open the project in [GitHub Codespaces](#open-in-github-codespaces), [VS Code Dev Containers](#open-in-dev-container), or [Local environment](#local-environment).
2. [Deploy from scratch](#deploy-from-scratch) or [deploy with existing Azure resources](#deploy-with-existing-azure-resources).
3. Copy `.env` file, located under `.azure/<environment name>/.env` folder to a new `.env` file in the project root folder where `README.md` file is.
4. Install the required packages:

```bash
pip install --upgrade -r requirements_dev.txt
```
5. Navigate to `/app/frontend` folder `cd /app/frontend`.
6. Run the UI app with the `streamlit run app.py` command. Frontend app uses the backend API deployed in Azure automatically.

### Deploy from scratch

If you don't have any pre-existing Azure services and want to start from a fresh deployment, execute the following commands.

1. Open a terminal.
2. Run `azd up` - This will provision Azure resources and deploy the sample project to those resources. We're using **[Bicep](https://learn.microsoft.com/azure/azure-resource-manager/bicep/overview?tabs=bicep&WT.mc_id=javascript-0000-cxa)**, a language that simplifies the definition of ARM templates and configuring Azure resources.
3. You keep `EVENT_HUBS_NAMESPACE_CONNECTION_STRING` and `AZURE_OPENAI_API_KEY` empty. We will assign them later after the first successful deployment.

![Deployment step 1](/assets/deployment-step-1.png)

![Deployment step 2](/assets/deployment-step-2.png)

After the application has been successfully deployed you will see URLs for both backend and frontend apps printed to the console.

![Deployment step 3](/assets/deployment-step-3.png)

> NOTE: It may take 5-10 minutes for the application to be fully deployed.

4. After the first deployment, we set environment variable values for `EVENT_HUBS_NAMESPACE_CONNECTION_STRING` and `AZURE_OPENAI_API_KEY` by running below commands. See how to retrieve [Azure OpenAI API Key](https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart?tabs=command-line%2Cpython&pivots=programming-language-python#retrieve-key-and-endpoint) and [Event Hubs connection string](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-get-connection-string). You can also manually set these values from the Azure portal and skip Step 7.

```bash
azd env set AZURE_OPENAI_API_KEY {Azure OpenAI API Key}

azd env set EVENT_HUBS_NAMESPACE_CONNECTION_STRING {Azure Event Hubs Namespace Connection String}
```

5. Run `azd deploy` to update these values in the Azure Container App. Pathway LLM App backend uses these environment variables. Other variables will be filled automatically.

![Deployment step 4](/assets/deployment-step-4.png)

6. Follow the generated link in the terminal for the frontend app in the Azure Container app and start to use the app. App ingests data from Azure event hubs. Learn how to send events using [Azure Event Hubs Data Generator](https://learn.microsoft.com/en-us/azure/event-hubs/send-and-receive-events-using-data-generator).

![Customer support and sentiment analysis dashboard](/assets/sentiment-analysis-demo.gif)


### Deploy with existing Azure resources

If you already have existing Azure resources, you can re-use those by setting `azd` environment values.

#### Existing Azure resource group

1. Run `azd env set AZURE_RESOURCE_GROUP {Name of existing resource group}`
2. Run `azd env set AZURE_LOCATION {Location of existing resource group}`

#### Existing Azure OpenAI resource

1. Run `azd env set AZURE_OPENAI_SERVICE {Name of existing OpenAI service}`
2. Run `azd env set AZURE_OPENAI_RESOURCE_GROUP {Name of existing resource group that OpenAI service is provisioned to}`
3. Run `azd env set AZURE_OPENAI_CHATGPT_DEPLOYMENT {Name of existing ChatGPT deployment}`. Only needed if your ChatGPT deployment is not the default 'chat'.
4. Run `azd env set AZURE_OPENAI_EMB_DEPLOYMENT {Name of existing GPT embedding deployment}`. Only needed if your embedding deployment is not the default 'embedding'.

When you run `azd up` after and are prompted to select a value for `openAiResourceGroupLocation`, make sure to select the same location as the existing OpenAI resource group.
