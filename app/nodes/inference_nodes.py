from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.vectorstores import Chroma
from ..models.pydantic_models import SubQueryList, Critique
from ..core.config import CHROMA_DB_PATH

def decompose_query_node(state, llm_flash: ChatGoogleGenerativeAI):
    print("---DECOMPOSING QUERY---")
    prompt = f"""Decompose the following complex query into a series of simple, atomic sub-queries that can be answered by a vector store.
    Query: {state['query']}
    Output only the JSON object."""
    structured_llm = llm_flash.with_structured_output(SubQueryList)
    sub_query_list = structured_llm.invoke(prompt)
    return {"sub_queries": [sq.sub_query for sq in sub_query_list.sub_queries]}

def run_retrieval_node(state, embedding_model):
    print("---RUNNING RETRIEVAL---")
    vectorstore = Chroma(persist_directory=CHROMA_DB_PATH, embedding_function=embedding_model)
    retriever = vectorstore.as_retriever()
    retrieved_docs = []
    for sub_query in state['sub_queries']:
        retrieved_docs.extend(retriever.invoke(sub_query))
    unique_docs = {doc.page_content: doc for doc in retrieved_docs}
    return {"retrieved_context": list(unique_docs.values())}

def generate_answer_node(state, llm_flash: ChatGoogleGenerativeAI):
    print("---GENERATING ANSWER---")
    context = "\n\n".join([doc.page_content for doc in state['retrieved_context']])
    prompt = f"""Synthesize the following retrieved context to answer the user's query.
    Provide in-line citations using the source metadata.
    Query: {state['query']}
    Context:
{context}"""
    answer = llm_flash.invoke(prompt)
    return {"draft_answer": answer.content}

def critique_answer_node(state, llm_pro: ChatGoogleGenerativeAI):
    print("---CRITIQUING ANSWER---")
    prompt = f"""Critique the following draft answer based on the provided context for factual consistency and citation accuracy.
    Query: {state['query']}
    Context: {state['retrieved_context']}
    Draft Answer: {state['draft_answer']}
    Output only the JSON object."""
    structured_llm = llm_pro.with_structured_output(Critique)
    critique = structured_llm.invoke(prompt)
    return {"critique": critique}

def should_continue_node(state):
    if state["critique"].critique_status == "PASS":
        return "end"
    else:
        return "decompose_query"
