# Agentic Enterprise RAG System

**Note:** This project is a work in progress.

## Overview

This project is a fully autonomous, reusable **Multi-Agent RAG Framework** that answers complex, multi-source, domain-specific questions with citable accuracy. It showcases leadership in **Agentic AI**, **MLOps**, and **Scalable Cloud Architecture** using Google Cloud's Gemini API and LangGraph.

## Core Technologies

*   **Orchestration:** LangGraph
*   **LLMs:** Gemini API (gemini-1.5-flash, gemini-1.5-pro)
*   **Backend/API:** FastAPI
*   **Database:** ChromaDB
*   **Utilities:** Python, Unstructured, langchain-google-genai
*   **Deployment:** Docker (Planned)

## Code Structure

The codebase is organized into a modular structure:

*   `app/main.py`: The FastAPI application entry point.
*   `app/core/`: Contains the core agent logic and configuration.
*   `app/models/`: Contains all Pydantic data models.
*   `app/nodes/`: Contains the individual functions for each agentic node.
*   `app/graphs/`: Contains the LangGraph workflow definitions.

## Architecture

This project utilizes a two-graph architecture:

1.  **MLOps / Indexing Workflow:** Responsible for ingesting, cleaning, and indexing documents to create a robust knowledge base.
2.  **Inference / Query Workflow:** Responsible for receiving a user query and executing a multi-step reasoning process to deliver a verified, cited answer.

*Placeholder for the Two-Graph Architecture Diagram*

## Workflows

### Indexing Workflow (Agentic MLOps Pipeline)

1.  **Analyze Sources:** The **Source Analyst** agent generates a structured list of documents to be processed for a given topic.
2.  **Acquire Data:** The **Data Acquisition** agent dynamically chooses the best method to ingest the data, parsing PDFs, HTML, and tables, and attaching metadata.
3.  **Index Data:** The **Knowledge Indexer** agent performs recursive character splitting to optimize chunks, generates embeddings, and commits the chunks to the ChromaDB index.

### Inference Workflow

1.  **Decompose Query:** The **Planner Agent** breaks down a complex user query into sequential, targeted sub-queries.
2.  **Run Retrieval:** The **RAG Tool Runner** executes the sub-queries against the ChromaDB index and aggregates the results.
3.  **Generate Answer:** The **Synthesizer Agent** fuses the retrieved context into a single, cohesive, non-hallucinated answer with in-line citations.
4.  **Critique Answer:** The **Reviewer Agent** reviews the answer for factual consistency and citation audit. If the critique fails, the process is looped back to the decomposition step.

*Placeholder for a GIF of a complex query execution*

## How to Run

1.  **Clone the repository:**
    ```bash
    git clone <your-repo-url>
    cd GCP-Agentic-Knowledge-Pipeline
    ```

2.  **Set up your environment:**
    Create a `.env` file in the root of the project and add your GCP Project ID and Gemini API Key:
    ```
    GCP_PROJECT_ID="your-gcp-project-id"
    GEMINI_API_KEY="your-gemini-api-key"
    ```

3.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

4.  **Run the application:**
    ```bash
    uvicorn app.main:app --reload
    ```

<!--
**Note:** Docker support will be available once feature development is complete.

3.  **Build and run the Docker container:**
    ```bash
    docker build -t rag-agent .
    docker run -p 80:80 -v ./db:/app/db --env-file .env rag-agent
    ```
-->

## API Endpoints

### Ingest Data

*   **Endpoint:** `/ingest`
*   **Method:** `POST`
*   **Purpose:** Triggers the MLOps Indexing Workflow to build or update the vector store.
*   **Request Body:**
    ```json
    {
        "topic": "your-topic"
    }
    ```

### Query Agent

*   **Endpoint:** `/query`
*   **Method:** `POST`
*   **Purpose:** Triggers the Inference Workflow and returns the final, verified, citable answer.
*   **Request Body:**
    ```json
    {
        "query": "your-complex-query"
    }
    ```

## Contributing

Contributions are welcome! Please feel free to open an issue or submit a pull request.
