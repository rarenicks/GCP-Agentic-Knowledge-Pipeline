from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from ..graphs.indexing_graph import create_indexing_graph
from ..graphs.inference_graph import create_inference_graph
from ..models.pydantic_models import IndexerState, AgentState
import os
from dotenv import load_dotenv

load_dotenv()



class EnterpriseRagAgent:
    def __init__(self):
        self.llm_pro = ChatGoogleGenerativeAI(model="gemini-2.5-pro", google_api_key=os.getenv("GEMINI_API_KEY"))
        self.llm_flash = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=os.getenv("GEMINI_API_KEY"))
        self.embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=os.getenv("GEMINI_API_KEY"))
        self.indexing_graph_app = create_indexing_graph(self.llm_pro, self.embedding_model)
        self.inference_graph_app = create_inference_graph(self.llm_pro, self.llm_flash, self.embedding_model)

    def ingest(self, topic: str):
        inputs = {"topical_domain": topic, "indexing_status": "PENDING"}
        return self.indexing_graph_app.invoke(inputs)

    def query(self, query: str):
        inputs = {"query": query}
        return self.inference_graph_app.invoke(inputs)