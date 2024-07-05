from datasets import load_dataset
from transformers import AutoModelForSeq2SeqLM
from transformers import AutoTokenizer
from transformers import GenerationConfig

DATASET_NAME = "knkarthick/dialogsum"
MODEL_NAME = 'google/flan-t5-base'

class ProcessNotes:

    def __init__(self, dataset_name, model_name):
        self.dataset = load_dataset(dataset_name)
        self.model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
        self.tokenizer = AutoTokenizer.from_pretrained(model_name, use_fast=True)
    

    def generate_summary(self, input_notes):
        prompt = f"""
        Summarize the following conversation.

        {input_notes}

        Summary:
            """

        # Input constructed prompt instead of the dialogue.
        inputs = self.tokenizer(prompt, return_tensors='pt')
        output = self.tokenizer.decode(
            self.model.generate(
                inputs["input_ids"], 
                max_new_tokens=50,
            )[0], 
            skip_special_tokens=True
        )
        
        return output

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
    