import sys
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from database.db import get_connection

#--------------------------------
#   CATALOGO DE ASSETS
#   15 assets que el scraper va a trackear
#--------------------------------
ASSETS = [
    #stocks
    {"symbol": "AAPL", "name":"Apple Inc.",     "category": "stocks"}, 
    {"symbol": "MSFT", "name": "Microsoft Corp.",    "category": "stocks"},
    {"symbol": "GOOGL", "name": "Alphabet Inc.",    "category": "stocks"},
    {"symbol": "TSLA", "name": "Tesla Inc.",    "category": "stocks"},
    {"symbol": "NVDA", "name": "NVIDIA Corp.",    "category": "stocks"},
    
    # Crypto
    {"symbol": "BTC-USD", "name": "Bitcoin",    "category": "crypto"},
    {"symbol": "ETH-USD", "name": "Ethereum",    "category": "crypto"},
    {"symbol": "SOL-USD", "name": "Solana",    "category": "crypto"},
    
    #Commodities
    {"symbol": "GC=F", "name": "Gold Futures",    "category": "commodities"},
    {"symbol": "CL=F", "name": "Crude Oil Futures",    "category": "commodities"},
    {"symbol": "SI=F", "name": "Silver Futures",    "category": "commodities"},
    
    #ETF's
    {"symbol": "SPY", "name": "S&P 500 ETF",    "category": "etfs"},
    {"symbol": "QQQ", "name": "NASDAQ 100 ETF",    "category": "etfs"},
    {"symbol": "VTI", "name": "Vanguard Total Market",    "category": "etfs"},
    {"symbol": "GLD", "name": "Gold ETF",    "category": "etfs"},
]

def seed_assets():
    """
    Inserta los activos en la tabla assets si no existen
    Usa INSERT OR IGNORE para no duplicar si ya están registrados
    """
    conn = get_connection()
    cursor = conn.cursor()
    
    for asset in ASSETS:
        cursor.execute(
            "IF NOT EXISTS (SELECT 1 FROM assets WHERE symbol = ?) "
            "INSERT INTO assets (symbol, name, category) VALUES (?,?,?)",
            (asset["symbol"], asset["symbol"], asset["name"], asset["category"])
        )
        
    conn.commit()
    conn.close()
    print(f"{len(ASSETS)} assets loaded into the database")
    
def get_all_assets():
    """ Reutrns all active asset sas a list of dicts"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id, symbol, name, category FROM assets WHERE active = 1")
    columns = [column[0] for column in cursor.description]
    rows = cursor.fetchall()
    conn.close()
    return [dict(zip(columns, row)) for row in rows]

if __name__ == "__main__":
    seed_assets()
    

