from typing import List, Literal
from langchain_core.pydantic_v1 import BaseModel, Field

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
