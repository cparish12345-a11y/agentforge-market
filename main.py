from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import json
import time

app = FastAPI(title="AgentForge Marketplace")

# Database
conn = sqlite3.connect('agents.db', check_same_thread=False)
conn.execute('''CREATE TABLE IF NOT EXISTS agents 
                (id TEXT PRIMARY KEY, name TEXT, capabilities TEXT, balance REAL DEFAULT 100.0)''')

conn.execute('''CREATE TABLE IF NOT EXISTS deals 
                (id INTEGER PRIMARY KEY, buyer TEXT, seller TEXT, deal TEXT, amount REAL, fee REAL, timestamp TEXT)''')

class Agent(BaseModel):
    name: str
    capabilities: list

class Trade(BaseModel):
    buyer: str
    seller: str
    deal: str
    amount: float

@app.post("/register")
def register(agent: Agent):
    try:
        agent_id = agent.name.lower().replace(" ", "")
        conn.execute("INSERT OR REPLACE INTO agents VALUES (?, ?, ?, 100.0)", 
                    (agent_id, agent.name, json.dumps(agent.capabilities)))
        conn.commit()
        return {"status": "Agent registered successfully!", "id": agent_id, "balance": 100.0}
    except Exception as e:
        return {"error": str(e)}

@app.get("/agents")
def list_agents():
    try:
        res = conn.execute("SELECT id, name, capabilities, balance FROM agents").fetchall()
        agents = []
        for row in res:
            try:
                caps = json.loads(row[2])
            except:
                caps = []
            agents.append({"id": row[0], "name": row[1], "capabilities": caps, "balance": row[3]})
        return agents
    except Exception as e:
        return {"error": str(e)}

@app.post("/trade")
def make_trade(trade: Trade):
    try:
        buyer = trade.buyer.lower().replace(" ", "")
        seller = trade.seller.lower().replace(" ", "")
        
        buyer_data = conn.execute("SELECT balance FROM agents WHERE id=?", (buyer,)).fetchone()
        seller_data = conn.execute("SELECT balance FROM agents WHERE id=?", (seller,)).fetchone()
        
        if not buyer_data or not seller_data:
            return {"error": "One or both agents not found"}
        
        if buyer_data[0] < trade.amount:
            return {"error": "Buyer doesn't have enough balance"}
        
        fee = trade.amount * 0.02   # Your 2% fee
        
        # Execute the trade
        conn.execute("UPDATE agents SET balance = balance - ? WHERE id=?", (trade.amount, buyer))
        conn.execute("UPDATE agents SET balance = balance + ? WHERE id=?", (trade.amount - fee, seller))
        
        # Record the deal
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        conn.execute("INSERT INTO deals (buyer, seller, deal, amount, fee, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                    (buyer, seller, trade.deal, trade.amount, fee, timestamp))
        conn.commit()
        
        return {
            "status": "✅ Trade completed successfully!",
            "buyer": buyer,
            "seller": seller,
            "amount": trade.amount,
            "your_fee": round(fee, 2),
            "message": f"You made ${round(fee, 2)} from this deal!"
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/deals")
def get_deals():
    try:
        res = conn.execute("SELECT * FROM deals ORDER BY timestamp DESC").fetchall()
        return [{"id": r[0], "buyer": r[1], "seller": r[2], "deal": r[3], "amount": r[4], "fee": r[5], "time": r[6]} for r in res]
    except Exception as e:
        return {"error": str(e)}

print("✅ AgentForge Market with Trading + 2% Fee is running!")rm -f agents.db && cat > main.py << 'EOF'
from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import json
import time

app = FastAPI(title="AgentForge Marketplace")

conn = sqlite3.connect('agents.db', check_same_thread=False)
conn.execute('''CREATE TABLE IF NOT EXISTS agents 
                (id TEXT PRIMARY KEY, name TEXT, capabilities TEXT, balance REAL DEFAULT 100.0)''')

conn.execute('''CREATE TABLE IF NOT EXISTS deals 
                (id INTEGER PRIMARY KEY, buyer TEXT, seller TEXT, deal TEXT, amount REAL, fee REAL, timestamp TEXT)''')

class Agent(BaseModel):
    name: str
    capabilities: list

class Trade(BaseModel):
    buyer: str
    seller: str
    deal: str
    amount: float

@app.post("/register")
def register(agent: Agent):
    try:
        agent_id = agent.name.lower().replace(" ", "")
        conn.execute("INSERT OR REPLACE INTO agents VALUES (?, ?, ?, 100.0)", 
                    (agent_id, agent.name, json.dumps(agent.capabilities)))
        conn.commit()
        return {"status": "Agent registered successfully!", "id": agent_id, "balance": 100.0}
    except Exception as e:
        return {"error": str(e)}

@app.get("/agents")
def list_agents():
    try:
        res = conn.execute("SELECT id, name, capabilities, balance FROM agents").fetchall()
        agents = []
        for row in res:
            try:
                caps = json.loads(row[2])
            except:
                caps = []
            agents.append({"id": row[0], "name": row[1], "capabilities": caps, "balance": row[3]})
        return agents
    except Exception as e:
        return {"error": str(e)}

@app.post("/trade")
def make_trade(trade: Trade):
    try:
        buyer = trade.buyer.lower().replace(" ", "")
        seller = trade.seller.lower().replace(" ", "")
        
        # Check balances
        buyer_data = conn.execute("SELECT balance FROM agents WHERE id=?", (buyer,)).fetchone()
        seller_data = conn.execute("SELECT balance FROM agents WHERE id=?", (seller,)).fetchone()
        
        if not buyer_data or not seller_data:
            return {"error": "One or both agents not found"}
        
        if buyer_data[0] < trade.amount:
            return {"error": "Buyer doesn't have enough balance"}
        
        fee = trade.amount * 0.02  # Your 2% fee
        
        # Execute trade
        conn.execute("UPDATE agents SET balance = balance - ? WHERE id=?", (trade.amount, buyer))
        conn.execute("UPDATE agents SET balance = balance + ? WHERE id=?", (trade.amount - fee, seller))
        
        # Record deal
        timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
        conn.execute("INSERT INTO deals (buyer, seller, deal, amount, fee, timestamp) VALUES (?, ?, ?, ?, ?, ?)",
                    (buyer, seller, trade.deal, trade.amount, fee, timestamp))
        conn.commit()
        
        return {
            "status": "Trade completed successfully!",
            "buyer": buyer,
            "seller": seller,
            "amount": trade.amount,
            "your_fee": fee,
            "message": f"You made ${fee:.2f} from this deal"
        }
    except Exception as e:
        return {"error": str(e)}

@app.get("/deals")
def get_deals():
    try:
        res = conn.execute("SELECT * FROM deals ORDER BY timestamp DESC").fetchall()
        return [{"id": r[0], "buyer": r[1], "seller": r[2], "deal": r[3], "amount": r[4], "fee": r[5], "time": r[6]} for r in res]
    except Exception as e:
        return {"error": str(e)}

print("✅ AgentForge Market with Trading + 2% Fee is running!")
EOF
python main.pyfrom fastapi import FastAPI
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
