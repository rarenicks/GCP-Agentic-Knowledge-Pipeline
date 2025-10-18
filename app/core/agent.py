from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from ..graphs.indexing_graph import create_indexing_graph
from ..graphs.inference_graph import create_inference_graph
from typing import TypedDict, List, Literal

class IndexerState(TypedDict):
    topical_domain: str
    documents_to_process: List[dict]
    raw_documents: List[dict]
    indexing_status: Literal["PENDING", "SUCCESS", "FAILURE"]

class AgentState(TypedDict):
    query: str
    sub_queries: List[str]
    retrieved_context: List[dict]
    draft_answer: str
    critique: dict

class EnterpriseRagAgent:
    def __init__(self):
        self.llm_pro = ChatGoogleGenerativeAI(model="gemini-1.5-pro-latest")
        self.llm_flash = ChatGoogleGenerativeAI(model="gemini-1.5-flash-latest")
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
        self.indexing_graph_app = create_indexing_graph(self.llm_pro, self.embedding_model)
        self.inference_graph_app = create_inference_graph(self.llm_pro, self.llm_flash, self.embedding_model)

    def ingest(self, topic: str):
        inputs = {"topical_domain": topic, "indexing_status": "PENDING"}
        return self.indexing_graph_app.invoke(inputs)

    def query(self, query: str):
        inputs = {"query": query}
        return self.inference_graph_app.invoke(inputs)
