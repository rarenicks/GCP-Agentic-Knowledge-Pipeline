from typing import List, Literal, TypedDict
from pydantic import BaseModel, Field

class DocumentSource(BaseModel):
    title: str = Field(description="A descriptive title for the source.")
    url: str = Field(description="The direct, authoritative URL to the document.")
    doc_type: Literal["html", "pdf", "docx"] = Field(description="The file type expected at the URL.")
    context_level: Literal["national", "local", "guidance"] = Field(description="The level of authority or specificity.")

class DocumentSourceList(BaseModel):
    documents: List[DocumentSource]

class SubQuery(BaseModel):
    sub_query: str = Field(description="A specific, atomic query to be run against the vector store.")

class SubQueryList(BaseModel):
    sub_queries: List[SubQuery]

class Critique(BaseModel):
    critique_status: Literal["PASS", "FAIL"] = Field(description="The status of the critique.")
    critique_reasoning: str = Field(description="The reasoning for the critique status.")

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