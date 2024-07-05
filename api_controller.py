from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from process_notes import ProcessNotes

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Notes(BaseModel):
    text: str

@app.get("/")
async def hello():
   return {"message": "Hello World"}

@app.post("/summarize")
async def summarize(notes: Notes):
    process = ProcessNotes("knkarthick/dialogsum", "google/flan-t5-base")
    summary = process.generate_summary(notes.text)
    return {"summary": summary}