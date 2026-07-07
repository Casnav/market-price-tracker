import sys 
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

import yfinance as yf
from datetime import datetime
from database.db import get_connection
from database.models import get_all_assets

def get_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        data = ticker.fast_info
        
        price = round(data["lastPrice"], 4)
        open_price = round(data["open"], 4)     if data["open"] else None
        high_price = round(data["dayHigh"], 4)     if data["dayHigh"] else None
        low_price = round(data["dayLow"], 4)       if data["dayLow"] else None
        volume = int(data["threeMonthAverageVolume"]) if data["threeMonthAverageVolume"] else None
        prev_close = data["previousClose"]
        
        change_pct = None
        if prev_close and prev_close != 0:
            change_pct = round(((price - prev_close) / prev_close) * 100, 2)
        
        return {
            "price": price,
            "open_price": open_price,
            "high_price": high_price,
            "low_price": low_price,
            "volume": volume,
            "change_pct": change_pct
        }
    except Exception as e:
        print(f" ERROR obteniendo {symbol}: {e}")
        return None
    
def save_price(asset_id, price_data):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO price_history" 
        "(asset_id, price, open_price, high_price, low_price, volume, change_pct) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (
            asset_id,
            price_data["price"],
            price_data["open_price"],
            price_data["high_price"],
            price_data["low_price"],
            price_data["volume"],
            price_data["change_pct"]
        )
    )
    conn.commit()
    conn.close()

def save_log(status, assets_ok, assets_fail, message=None):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT INTO scrape_logs (status, assets_ok, assets_fail, message) "
        "VALUES (?,?,?,?)",
        (status, assets_ok, assets_fail, message)
    )
    conn.commit()
    conn.close()
    
    
def run_scraper():
    print(f"\n{'='*50}")
    print(f"    Scraper iniciado: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"\n{'='*50}")
    
    assets = get_all_assets()
    assets_ok = 0
    assets_fail = 0
    
    for asset in assets:
        symbol = asset["symbol"]
        name = asset["name"]
        print(f"    Obteniendo {symbol} ({name})...", end=" ")
        
        price_data = get_price(symbol)
        
        if price_data:
            save_price(asset["id"], price_data)
            print(f"{price_data['price']}   ({price_data['change_pct']}%)")
            assets_ok += 1
            
        else:
            print("ERROR")
            assets_fail += 1
            
    status = "success" if assets_fail == 0 else "partial"
    save_log(status, assets_ok, assets_fail)
    
    print(f"\n  Resultado: {assets_ok} ok / {assets_fail} fallidos")
    print(f"{'='*50}\n")


if __name__ == "__main__":
    run_scraper()
    
    
