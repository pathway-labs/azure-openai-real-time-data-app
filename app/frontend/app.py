import os
import requests
import streamlit as st
from dotenv import load_dotenv
import pandas as pd
import json
import time
import plotly.express as px

load_dotenv()
api_host = os.environ.get("BACKEND_API_URI", "http://127.0.0.1")

# Streamlit UI elements
st.title("Customer support and sentiment analysis dashboard")

st.subheader("Example prompt")

default_prompt = "Provide overall sentiment trends, and common topics and rating over time and sources with counts based on last feedback events and respond only in json without explanation and new line. Follow this json structure and replace values accordingly: {\"sentiment_trends\": {\"positive\": 3, \"negative\": 1, \"neutral\": 1}, \"common_topics\": [{\"topic\": \"customer service\", \"count\": 10}, {\"topic\": \"product quality\", \"count\": 7}], \"rating_over_time\": [{\"date\": \"2021-01-01\", \"rating\": 4.5}, {\"date\": \"2021-01-02\", \"rating\": 3.8}], \"common_sources\": [{\"source\": \"Online Survey\", \"count\": 20}, {\"source\": \"Customer Feedback Form\", \"count\": 15}]}"

st.text("Provide overall sentiment trends, and common topics and rating over time\n and sources with counts based on last feedback events")

url = f"{api_host}"
data = {"query": default_prompt, "user": "user"}

response = requests.post(url, json=data)

if response.status_code == 200:
    data_response = response.json()
    json_data = json.loads(data_response)
    
    # Sentiment Trends
    sentiment_df = pd.DataFrame(list(json_data["sentiment_trends"].items()), columns=['Sentiment', 'Count'])
    color_map = {"positive": "green", "negative": "red", "neutral": "blue"}
    fig_sentiment = px.bar(sentiment_df, x='Sentiment', y='Count', title="Sentiment Trends", color='Sentiment', color_discrete_map=color_map)
    
    # Rating Over Time
    # rating_data = []
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
    
else:
    st.error(
        f"Failed to send data to API. Status code: {response.status_code}"
    )
    
# Uncomment this to make real-time

# placeholder = st.empty()


# for seconds in range(200):
    
#     url = f"{api_host}"
#     data = {"query": default_prompt, "user": "user"}

#     response = requests.post(url, json=data)

#     if response.status_code == 200:
#         data_response = response.json()
#         json_data = json.loads(data_response)

#         with placeholder.container():
#             # Sentiment Trends
#             sentiment_df = pd.DataFrame(list(json_data["sentiment_trends"].items()), columns=['Sentiment', 'Count'])
#             color_map = {"positive": "green", "negative": "red", "neutral": "blue"}
#             fig_sentiment = px.bar(sentiment_df, x='Sentiment', y='Count', title="Sentiment Trends", color='Sentiment', color_discrete_map=color_map)

#             # Rating Over Time
#             rating_data = json_data["rating_over_time"]
#             rating_df = pd.DataFrame(rating_data)
#             rating_df['Date'] = pd.to_datetime(rating_df['date'])
#             fig_rating = px.line(rating_df, x='Date', y='rating', title="Average Rating Over Time", markers=True)

#             # Streamlit layout
#             st.plotly_chart(fig_sentiment, use_container_width=True)

#             st.plotly_chart(fig_rating, use_container_width=True)

#             # Convert the source counts to a DataFrame for visualization
#             sources_df = pd.DataFrame(json_data["common_topics"], columns=['topic', 'count'])
#             fig_sources = px.bar(sources_df, x='topic', y='count', title="Common Topics")
#             st.plotly_chart(fig_sources, use_container_width=True)

#             sources_df = pd.DataFrame(json_data["common_sources"], columns=['source', 'count'])
#             fig_sources = px.bar(sources_df, x='source', y='count', title="Common Sources")
#             st.plotly_chart(fig_sources, use_container_width=True)

#             time.sleep(2)

#     else:
#         st.error(
#             f"Failed to send data to API. Status code: {response.status_code}"
#         )
