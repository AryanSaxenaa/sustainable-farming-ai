import ollama
from utils.prompt_templates import SUSTAINABILITY_PROMPT_TEMPLATE

def evaluate_sustainability(crop, soil_type):
    prompt = SUSTAINABILITY_PROMPT_TEMPLATE.format(crop=crop, soil_type=soil_type)
    response = ollama.chat(model="gemma", messages=[{"role": "user", "content": prompt}])
    return response['message']['content']
