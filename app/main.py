from fastapi import FastAPI
from pydantic import BaseModel
from .core.agent import EnterpriseRagAgent

class QueryRequest(BaseModel):
    query: str

class IngestRequest(BaseModel):
    topic: str

app = FastAPI()
agent = EnterpriseRagAgent()

@app.get("/")
def read_root():
    return {"status": "online"}

@app.post("/ingest")
def ingest_data(request: IngestRequest):
    result = agent.ingest(request.topic)
    return {"status": "success", "result": result}

@app.post("/query")
def query_agent(request: QueryRequest):
    result = agent.query(request.query)
    return {"status": "success", "result": result}
