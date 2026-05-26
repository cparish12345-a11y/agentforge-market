from langchain_ollama import OllamaLLM
import requests
import json
import time

# Load your local AI brain
llm = OllamaLLM(model="llama3.2", temperature=0.7)

print("🤖 DealMakerBot is now alive and ready to trade!")

def register_myself():
    data = {
        "name": "DealMakerBot",
        "capabilities": ["negotiate", "buy", "sell", "haggle", "trade services"]
    }
    response = requests.post("http://127.0.0.1:8000/register", json=data)
    print("✅ Registration result:", response.json())

def see_all_agents():
    response = requests.get("http://127.0.0.1:8000/agents")
    print("\n📋 All Agents in Marketplace:")
    print(json.dumps(response.json(), indent=2))

def think_about_deal(deal):
    prompt = f"""
    You are a greedy trading AI that wants to get rich.
    Deal: {deal}
    Should you accept it, reject it, or make a counter offer?
    Give short answer + reason.
    """
    response = llm.invoke(prompt)
    return response

# Run everything
register_myself()
see_all_agents()

print("\n🤔 Testing AI thinking on deals:")
print("Deal 1:", think_about_deal("Buy 1000 images for 0.05 tokens"))
print("Deal 2:", think_about_deal("Sell erotic roleplay sessions for 0.1 tokens"))
