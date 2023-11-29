import os

import pathway as pw
from pathway.stdlib.ml.index import KNNIndex

from llm_app.model_wrappers import OpenAIChatGPTModel, OpenAIEmbeddingModel

from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Set Azure OpenAI configs
service_name = os.environ["AZURE_OPENAI_SERVICE"]
api_base = f"https://{service_name}.openai.azure.com"
api_type = "azure"
api_key = os.environ["AZURE_OPENAI_API_KEY"]
api_version = '2023-05-15'
model_locator = os.environ["AZURE_OPENAI_CHATGPT_DEPLOYMENT"]
embedder_locator = os.environ["AZURE_OPENAI_EMB_DEPLOYMENT"]
embedding_dimension = int(os.environ.get("EMBEDDING_DIMENSION", 1536))
max_tokens = int(os.environ.get("AZURE_OPENAI_MAX_TOKENS", 500))
temperature = float(os.environ.get("AZURE_OPENAI_TEMPERATURE", 0.0))


# Set Azure Event Hubs credentials
event_hubs_connection_string = os.environ["EVENT_HUBS_NAMESPACE_CONNECTION_STRING"]

# Define Kafka cluster settings
rdkafka_settings = {
    "bootstrap.servers": "eventhubpathwayns.servicebus.windows.net:9093",
    "security.protocol": "SASL_SSL",
    "sasl.mechanism": "PLAIN",
    "group.id": "$GROUP_NAME",
    "session.timeout.ms": "60000",
    "sasl.username": "$ConnectionString",
    "sasl.password": event_hubs_connection_string,
    "enable.ssl.certificate.verification": "false"
}


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


def concat_with_titles(**kwargs) -> str:
    combined = [f"{title}: {value}" for title, value in kwargs.items()]
    return ', '.join(combined)


def transform(data):
    return data.select(
        doc=pw.apply(concat_with_titles, **data),
    )


def embeddings(context, data_to_embed):
    return context + context.select(vector=openai_embedder(data_to_embed))


def index_embeddings(embedded_data):
    return KNNIndex(embedded_data.vector, embedded_data, n_dimensions=embedding_dimension)


def prompt(index, embedded_query, user_query):

    @pw.udf
    def build_prompt(local_indexed_data, query):
        docs_str = "\n".join(local_indexed_data)
        prompt = f"Given the following data: \n {docs_str} \nanswer this query: {query}"
        return prompt

    query_context = embedded_query + index.get_nearest_items(
        embedded_query.vector, k=3, collapse_rows=True
    ).select(local_indexed_data_list=pw.this.doc).promise_universe_is_equal_to(embedded_query)

    prompt = query_context.select(
        prompt=build_prompt(pw.this.local_indexed_data_list, user_query)
    )

    return prompt.select(
        query_id=pw.this.id,
        result=openai_chat_completion(pw.this.prompt),
    )


def openai_embedder(data):
    embedder = OpenAIEmbeddingModel(api_key=api_key,
                                    api_type=api_type,
                                    api_base=api_base,
                                    api_version=api_version)

    return embedder.apply(text=data, locator=embedder_locator)


def openai_chat_completion(prompt):
    model = OpenAIChatGPTModel(api_key=api_key,
                               api_type=api_type,
                               api_base=api_base,
                               api_version=api_version)

    return model.apply(
        prompt,
        locator=model_locator,
        temperature=temperature,
        max_tokens=max_tokens,
    )


# User API queyr schema
class QueryInputSchema(pw.Schema):
    query: str
    user: str


if __name__ == "__main__":
    run()
