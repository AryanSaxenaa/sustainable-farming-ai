
### utils/embeddings.py
from ollama import Embedding

embed_model = Embedding(model="distilbert")

def generate_embedding(text):
    return embed_model.embed(text)