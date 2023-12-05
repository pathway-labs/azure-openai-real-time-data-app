# How to build a data streaming pipeline for real-time enterprise generative AI apps

Subtitle: How to build a data streaming pipeline for real-time enterprise generative AI apps using [Azure Event Hubs](https://learn.microsoft.com/en-us/azure/event-hubs/azure-event-hubs-kafka-overview) + [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service) + [Pathway](https://pathway.com/)’s [LLM App](https://github.com/pathwaycom/llm-app)+[Streamlit](https://streamlit.io/)

Real-time AI app needs real-time data to respond with the most up-to-date information to user queries or perform quick actions autonomously. For example, a customer support team wants to improve its customer support by analyzing customer feedback and inquiries in real-time. They aim to understand common issues, track customer sentiment, and identify areas for improvement in their products and services. To achieve this, they need a system that can process large data streams, analyze text for insights, and present these insights in an accessible way.

To help them we will build a [real-time data pipeline](https://github.com/pathway-labs/azure-openai-real-time-data-app) with [Azure Event Hubs](https://learn.microsoft.com/en-us/azure/event-hubs/azure-event-hubs-kafka-overview), [Pathway](https://github.com/pathwaycom/llm-app), and [Azure OpenAI](https://azure.microsoft.com/en-us/products/ai-services/openai-service). This integrated system leverages the strengths of Kafka for robust data processing, LLMs like GPT for advanced text analytics, and Streamlit for user-friendly data visualization. This combination empowers businesses to build and deploy enterprise AI applications that provide the freshest contextual visual data. The new solution can help to multiple teams:

- **Customer Support Team**: They can use the dashboard to monitor customer satisfaction and common issues in real-time, allowing for quick responses.
- **Product Development**: Insights from customer feedback can inform product development, highlighting areas for improvement or innovation.
- **Marketing and PR**: Understanding customer sentiment trends helps in tailoring marketing campaigns and managing public relations more effectively.

## Implementation

Let’s break down the main parts of the application architecture and understand the role of each in our solution. The project source code, deployment automation implementation, and setup guidelines can be found on [GitHub](https://github.com/pathway-labs/azure-openai-real-time-data-app).

1. **Azure Event Hubs & Kafka: Real-Time Data Streaming and Processing**
    
    Azure Event Hubs collects real-time data from various sources, such as customer feedback forms, support chat logs, and social media mentions. This data is then streamed into a Kafka cluster for further processing.
    
2. **Large Language Models (LLMs) like GPT from Azure OpenAI: Text Analysis and Sentiment Detection**
    
    The text data from Kafka is fed into an LLM for natural language processing using Pathway. This model performs sentiment analysis, key phrase extraction, and feedback categorization (e.g., identifying common issues or topics).
    
3. **Pathway to enable real-time data pipeline**
    
    Pathway gains access to the [data streams](https://pathway.com/developers/user-guide/concepts/welcome/) from Azure Event Hubs, it preprocesses, transforms, or joins them and the [LLM App](https://github.com/pathwaycom/llm-app) helps to bring real-time context to the AI App with real-time vector indexing, semantic search, and retrieval capabilities. The text content of the events will be sent to Azure OpenAI embedding APIs via the LLM App to compute the embeddings and vector representations will be indexed using [KNN (K-Nearest Neighbors)](https://pathway.com/developers/showcases/lsh/lsh_chapter1). Using the LLM app, the company can gain deep insights from unstructured text data, understanding the sentiment and nuances of customer feedback.
    
4. **Streamlit: Interactive Dashboard for Visualization**
    
    Streamlit is used to create an interactive web dashboard that visualizes the insights derived from customer feedback. This dashboard can show real-time metrics such as overall sentiment trends, and common topics in customer feedback, and even alert the team to emerging issues (See [example](https://github.com/pathwaycom/llm-app/tree/main/examples/pipelines/drive_alert) implementation of alerting to enhance this project).
    
    Here is a short demo of running the app in Azure:
    

![Untitled](/assets/sentiment-analysis-demo.gif)

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

As you can see in the below infrastructural diagram, we use two [Azure Container Apps](https://learn.microsoft.com/azure/container-apps/?WT.mc_id=javascript-0000-cxa) to deploy the Pathway LLM App and Streamlit UI dashboard to a single Azure Resource Group. 

![Untitled](/assets/azure-infra-architecture.png)

### Simple architecture and reduced costs

The current solution with the LLM App simplifies the AI pipeline infrastructure by consolidating capabilities into one platform. No need to integrate and maintain separate modules for your Gen AI app: ~~Vector Databases (e.g. Pinecone/Weaviate/Qdrant) + LangChain + Cache (e.g. Redis) + API Framework (e.g. Fast API)~~. It also reduced the cloud costs compared to other possible implementations using Vector Database/Azure Cognitive Search + Azure Functions (For hosting API and logic code) + Azure App Service. Let’s calculate it using the [Azure pricing calculator](https://azure.microsoft.com/en-us/pricing/calculator/). For simplicity, we do not count costs for Azure OpenAI.

1. In the current solution with two Azure Container Apps (10 million requests per month) + one Azure Event Hubs (10 million events per month), you can see the total estimated cost per month here which is around 11 USD with the basic setup.

See the report: https://azure.com/e/d3f1261757d14dc5a9ea1c414a00069f

2. In the second solution we use Azure Event Hubs + Azure Function (to ingest real-time events and logic code) + Azure AI Search (vector search) + Container Apps (To host Streamlit UI Dashboard). You will end with an estimated monthly cost of 17 USD per month. We did not count costs for Storage accounts required by Functions. As you can see, the 

See the report: https://azure.com/e/0c934b47b2b745f596d59121f4020677

3. You can try to estimate costs yourself for one of the famous solutions [ChatGPT + Enterprise data with Azure OpenAI and AI Search](https://github.com/Azure-Samples/azure-search-openai-demo) on GitHub and analyze how the same solution can be implemented using Pathway’s LLM App and it can be more efficient.

## Tutorial - Creating the app

The app development consists of two parts: backend API and frontend UI.

### Part 1: Design the Streamlit UI

We will start with constructing Streamlit UI and create a simple web application with Streamlit. It interacts with the LLM App backend service over REST API and displays the insights derived from real-time customer feedback. See the full source code in the [app.py](https://github.com/pathway-labs/azure-openai-real-time-data-app/blob/main/app/frontend/app.py) file. 

```jsx
st.title("Customer support and sentiment analysis dashboard")

st.subheader("Example prompt")

default_prompt = "Provide overall sentiment trends, and common topics and rating over time and sources with counts based on last feedback events"

st.text(default_prompt)

placeholder = st.empty()

for seconds in range(200):
    
    url = f"{api_host}"
    data = {"query": default_prompt, "user": "user"}

    response = requests.post(url, json=data)

    if response.status_code == 200:
        data_response = response.json()
        json_data = json.loads(data_response)

        with placeholder.container():
            # Sentiment Trends
            sentiment_df = pd.DataFrame(list(json_data["sentiment_trends"].items()), columns=['Sentiment', 'Count'])
            color_map = {"positive": "green", "negative": "red", "neutral": "blue"}
            fig_sentiment = px.bar(sentiment_df, x='Sentiment', y='Count', title="Sentiment Trends", color='Sentiment', color_discrete_map=color_map)

            # Rating Over Time
            rating_data = json_data["rating_over_time"]
            rating_df = pd.DataFrame(rating_data)
            rating_df['Date'] = pd.to_datetime(rating_df['date'])
            fig_rating = px.line(rating_df, x='Date', y='rating', title="Average Rating Over Time", markers=True)

            # Streamlit layout
            st.plotly_chart(fig_sentiment, use_container_width=True)

            st.plotly_chart(fig_rating, use_container_width=True)

            # Convert the source counts to a DataFrame for visualization
            sources_df = pd.DataFrame(json_data["common_topics"], columns=['topic', 'count'])
            fig_sources = px.bar(sources_df, x='topic', y='count', title="Common Topics")
            st.plotly_chart(fig_sources, use_container_width=True)

            sources_df = pd.DataFrame(json_data["common_sources"], columns=['source', 'count'])
            fig_sources = px.bar(sources_df, x='source', y='count', title="Common Sources")
            st.plotly_chart(fig_sources, use_container_width=True)

            time.sleep(1)

    else:
        st.error(
            f"Failed to send data to API. Status code: {response.status_code}"
        )
```

In the above code, we define a default prompt to instruct the LLM App to respond with all necessary data such as sentiment trends, common topics, ratings over time, and common sources as structured in JSON format.  We use [Streamlit Charts](https://docs.streamlit.io/library/api-reference/charts) to visualize different dashboards. The dashboards are updated every second, likely fetching and displaying new data each time.

### Part 2: Build a backend API

Next, we develop the backend logic where the app ingests streaming data from a Kafka topic provided by Azure Event Hubs and uses it to respond to user queries via an HTTP API. The function integrates with Azure OpenAI's Embeddings API for generating embeddings and a ChatGPT model for generating LLM responses. See the full source code in the [app.py](https://github.com/pathway-labs/azure-openai-real-time-data-app/blob/main/app/frontend/app.py) file. 

```jsx
...
def run(
    *,
    host: str = "0.0.0.0",
    port: int = 8080
):
    # Real-time data coming from the Kafka topic
    topic_data = pw.io.kafka.read(
        rdkafka_settings,
        topic="eventhubpathway",
        format="raw",
        autocommit_duration_ms=1000,
    )
    
    # Tranform data to structured document
    transformed_topic_data = transform(topic_data)

    # Compute embeddings for each Kafka event using the OpenAI Embeddings API
    embedded_topic_data = embeddings(context=transformed_topic_data,
                                     data_to_embed=transformed_topic_data.doc)

    # Construct an index on the generated embeddings in real-time
    index = index_embeddings(embedded_topic_data)

    # Given a user question as a query from your API
    query, response_writer = pw.io.http.rest_connector(
        host=host,
        port=port,
        schema=QueryInputSchema,
        autocommit_duration_ms=50,
    )
     
    # Generate embeddings for the query from the OpenAI Embeddings API
    embedded_query = embeddings(context=query, data_to_embed=pw.this.query)

    # Build prompt using indexed data
    responses = prompt(index, embedded_query, pw.this.query)

    # Feed the prompt to ChatGPT and obtain the generated answer.
    response_writer(responses)

    pw.run()
...
```

Generated vector embeddings are indexed for efficient retrieval in real-time. The user's query is embedded using the same embeddings API endpoint, to enable a vector search against the indexed Kafka data. Finally, a new prompt is constructed using the indexed data and the embedded user query. This prompt is then used to generate a response by querying a model like ChatGPT.

## What is next

As we have seen in the example of the customer feedback analysis app demo, used for businesses looking to harness real-time data for strategic decision-making and responsive customer service. This simplification in the architecture and implementation with Pathway’s LLM App means that your GenAI apps go to market within a short period (4-6 weeks), with lower costs and high security. Consider also visiting another showcase on **[Use LLMs for notifications](https://pathway.com/developers/showcases/llm-alert-pathway/#use-llms-for-notifications-crafting-a-rag-app-with-real-time-alerting)**. You will see a few examples showcasing different possibilities with the LLM App in the GitHub Repo. Follow the instructions in [Get Started with Pathway](https://github.com/pathwaycom/llm-app#get-started) to try out different demos.