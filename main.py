from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import json

app = FastAPI(title="AgentForge Market")

# Database setup
conn = sqlite3.connect('agents.db', check_same_thread=False)

conn.execute('''CREATE TABLE IF NOT EXISTS agents 
                (id TEXT PRIMARY KEY, 
                 name TEXT, 
                 capabilities TEXT)''')

class Agent(BaseModel):
    name: str
    capabilities: list

@app.post("/register")
def register(agent: Agent):
    try:
        agent_id = agent.name.lower().replace(" ", "")
        capabilities_json = json.dumps(agent.capabilities)
        
        conn.execute("INSERT OR REPLACE INTO agents VALUES (?, ?, ?)", 
                    (agent_id, agent.name, capabilities_json))
        conn.commit()
        
        return {"status": "Agent registered successfully!", "id": agent_id}
    except Exception as e:
        return {"error": str(e)}

@app.get("/agents")
def list_agents():
    try:
        res = conn.execute("SELECT * FROM agents").fetchall()
        agents = []
        for row in res:
            try:
                caps = json.loads(row[2])
            except:
                caps = []
            agents.append({
                "id": row[0], 
                "name": row[1], 
                "capabilities": caps
            })
        return agents
    except Exception as e:
        return {"error": str(e)}

print("✅ AgentForge Market is running!")