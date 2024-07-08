from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from process_query import ProcessQuery

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Query(BaseModel):
    text: str


@app.get("/")
async def hello():
    return {"message": "Hello World"}


@app.post("/invoke")
async def summarize(query: Query):
    process = ProcessQuery("gemma2")
    output = process.generate(query.text)
    rag_output = process.rag_generate(query.text)
    return {"output": output, "rag_output": rag_output}
