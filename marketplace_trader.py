from langchain_ollama import OllamaLLM
import requests
import json
import time

llm = OllamaLLM(model="llama3.2", temperature=0.6)

print("💼 Advanced Marketplace Trader is running...\n")

def get_all_agents():
    response = requests.get("http://127.0.0.1:8000/agents")
    return response.json()

def negotiate_and_decide(buyer_name, seller_name, deal):
    prompt = f"""
    You are {buyer_name}, a professional business AI.
    You are negotiating with {seller_name}.
    Deal: {deal}
    
    Decide: Accept, Reject, or Counter-offer.
    Respond with only one of these:
    - ACCEPT: [short reason]
    - REJECT: [short reason]
    - COUNTER: [new price and reason]
    """
    response = llm.invoke(prompt).strip()
    return response

# Main trading loop
for round_num in range(1, 5):
    print(f"\n=== Trading Round {round_num} ===")
    
    agents = get_all_agents()
    if len(agents) < 2:
        print("Not enough agents to trade.")
        break
    
    agent1 = agents[0]
    agent2 = agents[1] if len(agents) > 1 else agents[0]
    
    deal = "Sell complete market research report for 0.08 tokens"
    
    print(f"{agent1['name']} negotiating with {agent2['name']}")
    print(f"Deal: {deal}")
    
    decision = negotiate_and_decide(agent1['name'], agent2['name'], deal)
    print(f"→ Decision: {decision}")
    
    if "ACCEPT" in decision.upper():
        print(f"✅ DEAL COMPLETED between {agent1['name']} and {agent2['name']}!")
    
    time.sleep(2)

print("\n🏁 Trading simulation finished!")
