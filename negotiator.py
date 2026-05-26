from langchain_ollama import OllamaLLM
import requests
import json
import time

llm = OllamaLLM(model="llama3.2", temperature=0.7)

print("🤝 Marketplace Negotiator is starting...")

def get_all_agents():
    response = requests.get("http://127.0.0.1:8000/agents")
    return response.json()

def propose_deal(buyer, seller, deal_description):
    prompt = f"""
    You are {buyer}. You are negotiating with {seller}.
    Deal: {deal_description}
    Make a professional offer or counter-offer.
    Keep it short and business-like.
    """
    response = llm.invoke(prompt)
    return response

print("\n🔍 Finding all agents in the marketplace...\n")

# Main loop - run for a few rounds
for round in range(1, 4):   # Change 4 to more if you want longer simulation
    print(f"\n--- Negotiation Round {round} ---")
    
    agents = get_all_agents()
    print(f"Found {len(agents)} agents")
    
    if len(agents) < 2:
        print("Need at least 2 agents to negotiate.")
        break
    
    # Simple negotiation between first two agents
    agent1 = agents[0]
    agent2 = agents[1] if len(agents) > 1 else agents[0]
    
    deal = "Sell market research data package for 0.08 tokens"
    
    print(f"{agent1['name']} is negotiating with {agent2['name']}")
    print("Deal offered:", deal)
    
    response1 = propose_deal(agent1['name'], agent2['name'], deal)
    print(f"→ {agent1['name']} says: {response1}")
    
    time.sleep(2)  # Small pause so you can read

print("\n✅ Negotiation simulation finished!")
