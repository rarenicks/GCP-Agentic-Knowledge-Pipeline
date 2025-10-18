from langgraph.graph import StateGraph, END
from ..nodes.inference_nodes import (
    decompose_query_node, 
    run_retrieval_node, 
    generate_answer_node, 
    critique_answer_node, 
    should_continue_node
)
from ..core.agent import AgentState

def create_inference_graph(llm_pro, llm_flash, embedding_model):
    workflow = StateGraph(AgentState)
    workflow.add_node("decompose_query", lambda state: decompose_query_node(state, llm_flash))
    workflow.add_node("run_retrieval", lambda state: run_retrieval_node(state, embedding_model))
    workflow.add_node("generate_answer", lambda state: generate_answer_node(state, llm_flash))
    workflow.add_node("critique_answer", lambda state: critique_answer_node(state, llm_pro))
    workflow.set_entry_point("decompose_query")
    workflow.add_edge("decompose_query", "run_retrieval")
    workflow.add_edge("run_retrieval", "generate_answer")
    workflow.add_edge("generate_answer", "critique_answer")
    workflow.add_conditional_edges("critique_answer", should_continue_node, {"end": END, "decompose_query": "decompose_query"})
    return workflow.compile()
