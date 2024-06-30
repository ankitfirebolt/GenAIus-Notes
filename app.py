# Building the Backend with FastAPI

from fastapi import FastAPI
from pydantic import BaseModel
from langchain import LangChain

app = FastAPI()
lc = LangChain()

class InputText(BaseModel):
    text: str

@app.post("/process_text/")
async def process_text(input_text: InputText):
    response = lc.process_text(input_text.text)
    return {"response": response}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)