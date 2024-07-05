from datasets import load_dataset
import torch
from langchain_community.llms import Ollama


DATASET_NAME = "knkarthick/dialogsum"
MODEL_NAME = "gemma2"


class ProcessNotes:

    def __init__(self, dataset_name, model_name):
        self.dataset = load_dataset(dataset_name)
        self.llm = Ollama(model=MODEL_NAME)
    

    def generate_summary(self, input_notes):
        prompt = f"""
        Summarize the following conversation.

        {input_notes}

        Summary:
            """
        return self.llm.invoke(prompt)

if __name__ == '__main__':
    process_notes = ProcessNotes(DATASET_NAME, MODEL_NAME)

    example_indices = [200, 400]
    for i, index in enumerate(example_indices):
            dialogue = process_notes.dataset['test'][index]['dialogue']
            summary = process_notes.dataset['test'][index]['summary']
            output = process_notes.generate_summary(dialogue)
             
            dash_line = "--------------------------------"
            print(dash_line)
            print('Example ', i + 1)
            print(dash_line)
            print(f'INPUT:\n{dialogue}')
            print(dash_line)
            print(f'HUMAN SUMMARY:\n{summary}')
            print(dash_line)    
            print(f'MODEL GENERATION - ZERO SHOT:\n{output}\n')