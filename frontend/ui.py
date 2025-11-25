import streamlit as st
import requests
import json

# Backend URL (service name in docker-compose)
BACKEND_URL = "http://rag-agent:8000"

st.set_page_config(page_title="Agentic RAG Chatbot", page_icon="🤖", layout="wide")

st.title("🤖 Agentic RAG Knowledge Pipeline")

# Sidebar for Ingestion
with st.sidebar:
    st.header("📚 Knowledge Base")
    st.markdown("### 🚀 Supercharge your Agent")
    st.markdown("Ingest new topics using **locally fetched data sources** to retrieve the most up-to-date info.")
    
    # Initialize topics history
    if "ingested_topics" not in st.session_state:
        st.session_state.ingested_topics = []

    topic = st.text_input("Enter Topic", placeholder="e.g., UK GDPR")
    
    if st.button("Ingest Topic", type="primary"):
        if topic:
            with st.spinner(f"Ingesting '{topic}'... This may take a moment."):
                try:
                    response = requests.post(f"{BACKEND_URL}/ingest", json={"topic": topic})
                    if response.status_code == 200:
                        st.success(f"Successfully ingested: {topic}")
                        if topic not in st.session_state.ingested_topics:
                            st.session_state.ingested_topics.append(topic)
                    else:
                        st.error(f"Failed to ingest. Status: {response.status_code}")
                        st.error(response.text)
                except Exception as e:
                    st.error(f"Connection error: {e}")
        else:
            st.warning("Please enter a topic.")

    if st.session_state.ingested_topics:
        st.markdown("---")
        st.markdown("**Ingested Topics:**")
        for t in st.session_state.ingested_topics:
            st.markdown(f"- ✅ {t}")

# Main Chat Interface
st.header("💬 Chat with your Agent")

# Initialize chat history
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat messages from history on app rerun
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# React to user input
if prompt := st.chat_input("Ask a question about your ingested topics..."):
    # Display user message in chat message container
    st.chat_message("user").markdown(prompt)
    # Add user message to chat history
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Display assistant response in chat message container
    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        full_response = ""
        
        with st.spinner("Thinking..."):
            try:
                response = requests.post(f"{BACKEND_URL}/query", json={"query": prompt})
                if response.status_code == 200:
                    result = response.json()
                    # Extract the answer from the result structure
                    # Adjust this based on your actual API response format
                    if "result" in result and "draft_answer" in result["result"]:
                         full_response = result["result"]["draft_answer"]
                    elif "result" in result:
                         full_response = str(result["result"])
                    else:
                         full_response = str(result)

                    message_placeholder.markdown(full_response)
                else:
                    full_response = f"Error: {response.status_code} - {response.text}"
                    message_placeholder.error(full_response)
            except Exception as e:
                full_response = f"Connection error: {e}"
                message_placeholder.error(full_response)
        
        # Add assistant response to chat history
        st.session_state.messages.append({"role": "assistant", "content": full_response})
