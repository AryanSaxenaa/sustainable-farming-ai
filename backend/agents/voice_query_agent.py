from ollama import Chat
from utils.prompt_templates import VOICE_PROMPT
from .farmer_advisor import get_farm_advice
from .market_researcher import get_market_analysis
from .sustainability_metrics import get_sustainability_metrics

llm = Chat(model="flan-t5")  # Good for understanding queries

def handle_voice_query(user_input):
    # Ask the model to classify the intent
    response = llm.chat(messages=[
        {"role": "user", "content": f"What kind of query is this?\n{user_input}\nRespond with one word: 'farming', 'market', or 'sustainability'"}
    ])
    intent = response['message']['content'].lower()

    if "market" in intent:
        return get_market_analysis(user_input)
    elif "sustainability" in intent:
        return get_sustainability_metrics(user_input)
    else:
        return get_farm_advice(user_input)
