from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import UnstructuredURLLoader
from langchain_community.vectorstores import Chroma
from ..models.pydantic_models import DocumentSourceList
from ..core.config import CHROMA_DB_PATH, SOURCE_LIST_FILE
import json
import os

def analyze_sources_node(state, llm_pro: ChatGoogleGenerativeAI):
    if os.path.exists(SOURCE_LIST_FILE) and os.path.getsize(SOURCE_LIST_FILE) > 0:
        print("---LOADING SOURCES FROM PERSISTENT STORAGE---")
        with open(SOURCE_LIST_FILE, 'r') as f:
            source_list_json = json.load(f)
        documents = [doc for doc in source_list_json['documents']]
        return {"documents_to_process": documents}
    else:
        print("---ANALYZING SOURCES (RESEARCH CASE)---")
        prompt = f"""Identify the 5-6 most critical, authoritative sources for the topical domain: {state['topical_domain']}.
        Include statutory law, compliance guidance, and at least one local council policy example. Output only the JSON object."""
        structured_llm = llm_pro.with_structured_output(DocumentSourceList)
        document_source_list = structured_llm.invoke(prompt)
        with open(SOURCE_LIST_FILE, 'w') as f:
            f.write(document_source_list.model_dump_json(indent=2))
        documents = [doc.model_dump() for doc in document_source_list.documents]
        return {"documents_to_process": documents}

def acquire_data_node(state):
    print("---ACQUIRING DATA---")
    urls = [doc['url'] for doc in state['documents_to_process']]
    loader = UnstructuredURLLoader(urls=urls)
    docs = loader.load()
    return {"raw_documents": docs}

def index_data_node(state, embedding_model):
    print("---INDEXING DATA---")
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(state['raw_documents'])
    vectorstore = Chroma.from_documents(documents=splits, embedding=embedding_model, persist_directory=CHROMA_DB_PATH)
    return {"indexing_status": "SUCCESS"}
