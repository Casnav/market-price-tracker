import sys
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0,ROOT)
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from sqlalchemy import create_engine
from dotenv import load_dotenv

def get_engine():
    server   = os.getenv("SERVER")
    database = os.getenv("DATABASE")
    driver   = os.getenv("DRIVER").replace(" ", "+")
    connection_url = (
        f"mssql+pyodbc://{server}/{database}"
        f"?driver={driver}"
        f"&trusted_connection=yes"
    )
    return create_engine(connection_url)

#--------------------------
 # PAGE CONFIG
#--------------------------
st.set_page_config(
    page_title="Market Price Tracker",
    page_icon="📈",
    layout="wide"
)

#--------------------------
 # DATA FUNCTIONS
#--------------------------
def get_latest_prices():
    df = pd.read_sql("""
        SELECT symbol, name, category, price,
                high_price, low_price, volume, change_pct, scraped_at
        FROM vw_latest_prices
        ORDER BY category, symbol
    """, get_engine())
    return df

def get_best_worst():
    df = pd.read_sql("SELECT * FROM vw_best_worst", get_engine())
    return df

def get_price_history(symbol):
    df = pd.read_sql(f"""
        SELECT p.price, p.change_pct, p.scraped_at
        FROM price_history p
        INNER JOIN assets a ON a.id = p.asset_id
        WHERE a.symbol = '{symbol}'
        ORDER BY p.scraped_at ASC    
    """, get_engine())
    return df

def get_volatility():
    df = pd.read_sql("""
        SELECT symbol, name, category,
                max_price, min_price, price_range, volatility_pct
        FROM vw_most_volatile
        ORDER BY volatility_pct DESC
    """, get_engine())
    return df

def get_scraper_health():
    df = pd.read_sql("""
        SELECT TOP 10 status, assets_ok, assets_fail, ran_at
        FROM vw_scraper_health
    """, get_engine())
    return df

#--------------------------
 # HEADER
#--------------------------
st.title("Market Price Tracker")
st.caption("Real-Time financial data- Stocks, Crypto, Commodities and ETFs")
st.divider()

#--------------------------
 # SECTION 1: LATEST PRICES
#--------------------------
st.subheader("Latest Prices")
df_prices = get_latest_prices()

if not df_prices.empty:
    categories = ["stocks", "crypto", "commodities", "etfs"]
    tabs = st.tabs(["📊 Stocks", "🪙 Crypto", "🏗️ Commodities", "📦 ETFs"])
    
    for tab, category in zip(tabs, categories):
        with tab:
            df_cat = df_prices[df_prices["category"] == category].copy()
            df_cat["change_pct"] = df_cat["change_pct"].apply(
                lambda x: f"+{x}%"
            )
            df_cat = df_cat.rename(columns={
                "symbol":   "Symbol",
                "name":     "Name",
                "price":    "Price (USD)",
                "high_price":"High",
                "low_price": "Low",
                "change_pct": "Change %",
                "scraped_at": "Last Update"
            })
            st.dataframe(
                df_cat[["Symbol", "Name", "Price (USD)", "High", "Low", "Change %","Last Update"]],
                use_container_width=True,
                hide_index=True
            )

st.divider()

#--------------------------
 # SECTION 2: BEST & WORST PERFORMER
#--------------------------
st.subheader("Best & Worst Performer Today")

df_bw = get_best_worst()

if not df_bw.empty:
    col1, col2 = st.columns(2)
    
    best = df_bw[df_bw["performance"] == "Best"].iloc[0]
    worst = df_bw[df_bw["performance"] == "Worst"].iloc[0]
    
    with col1:
        st.success(f"**Best: {best['symbol']} - {best['name']}**")
        st.metric(label="Price", value=f"${best['price']}", delta=f"{best['change_pct']}")

    with col2:
        st.error(f"**Worst: {worst['symbol']} - {worst['name']}**")
        st.metric(label="Price", value=f"${worst['price']}", delta=f"{worst['change_pct']}")
        
st.divider()

#--------------------------
 # SECTION 3: PRICE HISTORY CHART
#--------------------------
st.subheader("Price History")

symbols = df_prices["symbol"].tolist()
selected = st.selectbox("Select an asset", symbols)

df_history = get_price_history(selected)

if not df_history.empty:
    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=df_history["scraped_at"],
        y=df_history["price"],
        mode="lines+markers",
        name=selected,
        line=dict(color="#0062c4", width=2),
        marker=dict(size=5)
    ))
    fig.update_layout(
        title=f"{selected} - Price Over Time",
        xaxis_title="Time",
        yaxis_title="Price (USD)",
        template="plotly_dark",
        height=450
    )
    st.plotly_chart(fig, use_container_width=True)
else:
    st.info("Not enough data yet - run the scraper a few more times.")
    
st.divider()

#--------------------------
 # SECTION 4: VOLATILITY RANKING
#--------------------------
st.subheader("Volatility Ranking (7 days)")

df_vol = get_volatility()

if not df_vol.empty:
    fig2 = px.bar(
        df_vol,
        x="symbol",
        y="volatility_pct",
        color="category",
        title="Volatility % by Asset (7-day price range / avg price)",
        labels={"volatility_pct": "Volatility %", "symbol": "Asset"},
        template="plotly_dark",
        height=400
    )
    st.plotly_chart(fig2, use_container_width=True)
    
st.divider()

#--------------------------
 # SECTION 5: SCRAPER HEALTH
#--------------------------
st.subheader("🔧 Scraper Health")

df_health = get_scraper_health()

if not df_health.empty:
    st.dataframe(df_health, use_container_width=True, hide_index=True)
    
#--------------------------
 # FOOTER
#--------------------------
st.caption("Built with Python | yfinance | SQL server | Streamlit | Plotly")

