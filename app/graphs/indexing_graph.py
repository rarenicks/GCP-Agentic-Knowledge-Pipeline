from langgraph.graph import StateGraph, END
from ..nodes.indexing_nodes import analyze_sources_node, acquire_data_node, index_data_node
from ..core.agent import IndexerState

def create_indexing_graph(llm_pro, embedding_model):
    workflow = StateGraph(IndexerState)
    workflow.add_node("analyze_sources", lambda state: analyze_sources_node(state, llm_pro))
    workflow.add_node("acquire_data", acquire_data_node)
    workflow.add_node("index_data", lambda state: index_data_node(state, embedding_model))
    workflow.set_entry_point("analyze_sources")
    workflow.add_edge("analyze_sources", "acquire_data")
    workflow.add_edge("acquire_data", "index_data")
    workflow.add_edge("index_data", END)
    return workflow.compile()
