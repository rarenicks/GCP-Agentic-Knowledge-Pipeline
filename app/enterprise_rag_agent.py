from typing import List, TypedDict, Literal
from langgraph.graph import StateGraph, END

# Phase 1: Indexing Workflow State
class IndexerState(TypedDict):
    topical_domain: str
    documents_to_process: List[dict]
    raw_documents: List[dict]  # Using dict instead of Document for simplicity
    indexing_status: Literal["PENDING", "SUCCESS", "FAILURE"]


# Phase 2: Inference Workflow State
class AgentState(TypedDict):
    query: str
    sub_queries: List[str]
    retrieved_context: List[dict]  # Using dict instead of Document for simplicity
    draft_answer: str
    critique_status: Literal["PASS", "FAIL", "RETRY"]


# Phase 1: Agentic MLOps Nodes
def analyze_sources(state: IndexerState):
    # TODO: Implement logic to generate the structured list of documents
    print("---ANALYZING SOURCES---")
    # For demo purposes, we'll use a predefined list
    documents = [
        {"title": "Tenant Fees Act 2019", "url": "https://www.legislation.gov.uk/ukpga/2019/4/contents", "type": "html"},
        {"title": "Landlord and Tenant Act 1954", "url": "https://www.legislation.gov.uk/ukpga/Eliz2/2-3/56/contents", "type": "html"},
    ]
    return {"documents_to_process": documents}


def acquire_data(state: IndexerState):
    # TODO: Implement logic to ingest data using UnstructuredURLLoader/UnstructuredFileLoader
    print("---ACQUIRING DATA---")
    # For demo, we'll just pass the documents through
    return {"raw_documents": state["documents_to_process"]}


def index_data(state: IndexerState):
    # TODO: Implement logic for Recursive Character Splitting, embedding, and storing in ChromaDB
    print("---INDEXING DATA---")
    return {"indexing_status": "SUCCESS"}


# Phase 2: Agentic Inference Nodes
def decompose_query(state: AgentState):
    # TODO: Implement logic to break down the complex query into sub-queries
    print("---DECOMPOSING QUERY---")
    return {"sub_queries": ["What are the tenant fees?", "What is the landlord and tenant act?"]}


def run_retrieval(state: AgentState):
    # TODO: Implement logic to execute sub-queries against the ChromaDB index
    print("---RUNNING RETRIEVAL---")
    return {"retrieved_context": [{"content": "some retrieved content"}]}


def generate_answer(state: AgentState):
    # TODO: Implement logic to fuse the retrieved context into a cohesive answer
    print("---GENERATING ANSWER---")
    return {"draft_answer": "This is a draft answer based on the retrieved content."}


def critique_answer(state: AgentState):
    # TODO: Implement logic to review the answer for factual consistency and citation audit
    print("---CRITIQUING ANSWER---")
    # For demo, we'll randomly pass or fail
    import random
    if random.random() > 0.5:
        print("---CRITIQUE PASSED---")
        return {"critique_status": "PASS"}
    else:
        print("---CRITIQUE FAILED---")
        return {"critique_status": "FAIL"}


def should_continue(state: AgentState):
    if state["critique_status"] == "PASS":
        return "end"
    else:
        return "decompose_query"

class EnterpriseRagAgent:
    def __init__(self):
        self.indexing_graph_app = self.create_indexing_graph().compile()
        self.inference_graph_app = self.create_inference_graph().compile()

    def create_indexing_graph(self):
        workflow = StateGraph(IndexerState)
        workflow.add_node("analyze_sources", analyze_sources)
        workflow.add_node("acquire_data", acquire_data)
        workflow.add_node("index_data", index_data)

        workflow.set_entry_point("analyze_sources")
        workflow.add_edge("analyze_sources", "acquire_data")
        workflow.add_edge("acquire_data", "index_data")
        workflow.add_edge("index_data", END)
        return workflow

    def create_inference_graph(self):
        workflow = StateGraph(AgentState)
        workflow.add_node("decompose_query", decompose_query)
        workflow.add_node("run_retrieval", run_retrieval)
        workflow.add_node("generate_answer", generate_answer)
        workflow.add_node("critique_answer", critique_answer)

        workflow.set_entry_point("decompose_query")
        workflow.add_edge("decompose_query", "run_retrieval")
        workflow.add_edge("run_retrieval", "generate_answer")
        workflow.add_edge("generate_answer", "critique_answer")
        workflow.add_conditional_edges(
            "critique_answer",
            should_continue,
            {
                "end": END,
                "decompose_query": "decompose_query",
            },
        )
        return workflow

    def ingest(self, topic: str):
        inputs = {"topical_domain": topic, "indexing_status": "PENDING"}
        return self.indexing_graph_app.invoke(inputs)

    def query(self, query: str):
        inputs = {"query": query}
        return self.inference_graph_app.invoke(inputs)
