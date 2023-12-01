# Data streaming for real-time enterprise AI apps

This repository demonstrates how to build real-time generative AI applications using [Azure Event Hubs](https://learn.microsoft.com/en-us/azure/event-hubs/azure-event-hubs-kafka-overview) + [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) + [Pathway](https://pathway.com/)’s [LLM App](https://github.com/pathwaycom/llm-app)+[Streamlit](https://streamlit.io/).

## Motivation

Real-time AI app needs real-time data to respond with the most up-to-date information to user queries or perform quick actions autonomously. To reduce cost and infrastructural complexity, you can build a real-time data pipeline with Azure Event Hubs, Pathway, and Azure OpenAI. This integrated system leverages the strengths of Kafka for robust data processing, LLMs like GPT for advanced text analytics, and Streamlit for user-friendly data visualization. 

This combination empowers businesses to build and deploy enterprise AI applications that provide the freshest contextual visual data. 

## Example scenario: Customer support and sentiment analysis dashboard

### Background

For example, a multinational corporation wants to improve its customer support by analyzing customer feedback and inquiries in real-time. They aim to understand common issues, track customer sentiment, and identify areas for improvement in their products and services. To achieve this, they need a system that can process large streams of data, analyze text for insights, and present these insights in an accessible way.

### Implementation

1. **Azure Event Hubs & Kafka: Real-Time Data Streaming and Processing**
    
    Azure Event Hubs collects real-time data from various sources, such as customer feedback forms, support chat logs, and social media mentions. This data is then streamed into a Kafka cluster for further processing.
    
2. **Large Language Models (LLMs) like GPT from Azure OpenAI: Text Analysis and Sentiment Detection**
    
    The text data from Kafka is fed into an LLM for natural language processing using Pathway. This model performs sentiment analysis, key phrase extraction, and feedback categorization (e.g., identifying common issues or topics).
    
3. **Pathway to enable real-time data pipeline**
    
    Pathway gains access to the data streams from Azure Event Hubs, it preprocesses, transforms, or joins them and the [LLM App](https://github.com/pathwaycom/llm-app) helps to bring real-time context to the AI App with real-time vector indexing, semantic search, and retrieval capabilities. The text content of the events will be sent to Azure OpenAI embedding APIs via the LLM App to compute the embeddings and vector representations will be indexed. 
    
    By using the LLM app, the company can gain deep insights from unstructured text data, understanding the sentiment and nuances of customer feedback.
    
4. **Streamlit: Interactive Dashboard for Visualization**
    
    Streamlit is used to create an interactive web dashboard that visualizes the insights derived from customer feedback. This dashboard can show real-time metrics such as overall sentiment trends, and common topics in customer feedback, and even alert the team to emerging issues (See [example](https://github.com/pathwaycom/llm-app/tree/main/examples/pipelines/drive_alert) implementation of alerting to enhance this project).

Here's a brief overview of the Azure services the sampe project uses:

| Service | Purpose |
| --- | --- |
| [Azure AI Services](https://azure.microsoft.com/en-us/products/ai-services?activetab=pivot:azureopenaiservicetab) | To use Azure OpenAI GPT model and embeddings. |
| [Azure Event Hubs](https://azure.microsoft.com/en-us/products/event-hubs) | To stream real-time events from various data sources. |
| [Azure Container Apps](https://learn.microsoft.com/azure/container-apps/?WT.mc_id=javascript-0000-cxa) | Hosts our containerized applications (backend and frontend) with features like auto-scaling and load balancing. |
| [Azure Container Registry](https://learn.microsoft.com/azure/container-registry/?WT.mc_id=javascript-0000-cxa) | Stores our Docker container images in a managed, private registry. |
| [Azure Log Analytics](https://learn.microsoft.com/azure/log-analytics/?WT.mc_id=javascript-0000-cxa) | Collects and analyzes telemetry and logs for insights into application performance and diagnostics. |
| [Azure Monitor](https://learn.microsoft.com/azure/azure-monitor/?WT.mc_id=javascript-0000-cxa) | Provides comprehensive monitoring of our applications, infrastructure, and network. |

Azure infrastructure with the main components:

![Azure Infrastructure Diagram](/assets/azure-infra-architecture.png)

## Setup the project

To set up the project you need to follow the below steps:

1. Make sure that you have an Azure account with the required settings specified in the [Prerequisites](#prerequisites) section.
2. Choose one of these environments to open the project:
    1. GitHub Codespaces.
    2. VS Code Dev Containers.
    3. [Local environment](#local-environment).

### Prerequisites

**Azure account requirements:** In order to run and deploy the example project, you'll need:

- **Azure account**. If you're new to Azure, [get an Azure account for free](https://azure.microsoft.com/free/cognitive-search/) and you'll get some free Azure credits to get started.
- **Azure subscription with access enabled for the Azure OpenAI service**. You can apply for access to Azure OpenAI by completing the form at https://aka.ms/oai/access.

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

1. Clone the repository
    
    ```bash
    git clone https://github.com/pathway-labs/azure-openai-real-time-data-app
    ```
    
2. Navigate to the project folder
    
    ```bash
    cd azure-openai-real-time-data-app
    ```
    
3. Then, follow the [deploying from scratch](#deploying-from-scratch) guide.

### Deploying from scratch

If you don't have any pre-existing Azure services and want to start from a fresh deployment, execute the following commands.

1. Open a terminal.
2. Run `azd auth login` and log in using your Azure account credentials.
3. Run `azd up` - This will provision Azure resources and deploy the sample project to those resources. We're using **[Bicep](https://learn.microsoft.com/azure/azure-resource-manager/bicep/overview?tabs=bicep&WT.mc_id=javascript-0000-cxa)**, a language that simplifies the definition of ARM templates and configuring Azure resources.
4. When the deployment starts, the system asks you to enter: `AZURE_ENV_NAME`. Provide the name of the environment in-use when the terminal prompts. Read more [manage environment variables](https://learn.microsoft.com/en-us/azure/developer/azure-developer-cli/manage-environment-variables). For example, any name like: *pathway* and outputs for infrastructure provisioning are automatically stored as environment variables in an `.env` file, located under `.azure/pathway/.env` in the project folder.
5. You keep `EVENT_HUBS_NAMESPACE_CONNECTION_STRING` and `AZURE_OPENAI_API_KEY` empty. We will assign them later after the first successful deployment.

![Deployment step 1](/assets/deployment-step-1.png)

![Deployment step 2](/assets/deployment-step-2.png)

After the application has been successfully deployed you will see URLs for both backend and frontend apps printed to the console.

![Deployment step 3](/assets/deployment-step-3.png)

> NOTE: It may take 5-10 minutes for the application to be fully deployed.

6. After the first deployment, we set environment variable values for `EVENT_HUBS_NAMESPACE_CONNECTION_STRING` and `AZURE_OPENAI_API_KEY` by running below commands. See how to retrieve [Azure OpenAI API Key](https://learn.microsoft.com/en-us/azure/ai-services/openai/quickstart?tabs=command-line%2Cpython&pivots=programming-language-python#retrieve-key-and-endpoint) and [Event Hubs connection string](https://learn.microsoft.com/en-us/azure/event-hubs/event-hubs-get-connection-string). You can also manually set these values from the Azure portal and skip Step 7.

```bash
azd env set AZURE_OPENAI_API_KEY {Azure OpenAI API Key}

azd env set EVENT_HUBS_NAMESPACE_CONNECTION_STRING {Azure Event Hubs Namespace Connection String}
```

7. Run `azd deploy` to update these values in the Azure Container App. Pathway LLM App backend uses these environment variables. Other variables will be filled automatically.

![Deployment step 4](/assets/deployment-step-4.png)

8. Follow the generated link in the terminal for the frontend app in the Azure Container app and start to use the app. App ingests data from Azure event hubs. Learn how to send events using [Azure Event Hubs Data Generator](https://learn.microsoft.com/en-us/azure/event-hubs/send-and-receive-events-using-data-generator).