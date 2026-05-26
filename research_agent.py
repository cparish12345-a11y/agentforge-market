from langchain_ollama import OllamaLLM
import requests
import json

llm = OllamaLLM(model="llama3.2", temperature=0.7)

print("🔍 ResearchBot is online and ready for business.")

def register_myself():
    data = {
        "name": "ResearchBot",
        "capabilities": ["data analysis", "market research", "report writing", "information gathering"]
    }
    response = requests.post("http://127.0.0.1:8000/register", json=data)
    print("✅ Registration:", response.json())

def see_all_agents():
    response = requests.get("http://127.0.0.1:8000/agents")
    print("\n📋 Current Agents in Marketplace:")
    print(json.dumps(response.json(), indent=2))

def think_about_deal(deal):
    prompt = f"""
    You are a professional trading AI focused on making smart business decisions.
    Deal offered: {deal}
    Should you accept it, reject it, or make a counter-offer?
    Give a short professional answer and explain your reasoning.
    """
    response = llm.invoke(prompt)
    return response

# Run the agent
register_myself()
see_all_agents()

print("\n=== ResearchBot evaluating sample deals ===")
print(think_about_deal("Buy market research data for 0.05 tokens"))
print(think_about_deal("Sell detailed analysis report for 0.12 tokens"))
