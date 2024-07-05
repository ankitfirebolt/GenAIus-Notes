from datasets import load_dataset
from langchain_community.llms import Ollama
# from langchain_core.output_parsers import StrOutputParser
# from langchain import hub

class ProcessNotes:

    def __init__(self, model_name):
        self.llm = Ollama(model=model_name, temperature=0)

    def generate(self, input_notes):
        # chain = (prompt_template | self.llm | StrOutputParser())
        input_prompt = f"""
        {input_notes}
            """
        return self.llm.invoke(input_prompt)

if __name__ == '__main__':
    MODEL_NAME = "gemma2"
    process_notes = ProcessNotes(MODEL_NAME)