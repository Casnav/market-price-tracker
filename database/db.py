import pyodbc
import os
# --------------------------------
#   SQL SERVER CONNECTION CONFIG
# --------------------------------
SERVER = 'DESKTOP-RF3MTOQ'
DATABASE = 'market_tracker'
DRIVER = 'ODBC Driver 17 for SQL Server'

def get_connection():
    """Retorna una conexión a la base de datos SQLite"""
    conn = pyodbc.connect(
        f'DRIVER={{{DRIVER}}};'
        f'SERVER={SERVER};'
        f'DATABASE={DATABASE};'
        f'Trusted_Connection=yes;'    
    )
    return conn

def create_database():
    """Creates the database if it doesnt exist yet."""
    conn = pyodbc.connect(
        f'DRIVER={{{DRIVER}}};'
        f'SERVER={SERVER};'
        f'Trusted_Connection=yes;'
    )
    conn.autocommit = True
    cursor = conn.cursor()
    cursor.execute("""
        IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = 'market_tracker')
        CREATE DATABASE market_tracker
    """)
    conn.close()
    print("Database market_tracker ready.")

def init_db():
    """Creates all tables if they dont exist"""
    conn = get_connection()
    cursor = conn.cursor()
    
    #--------------------------------
    #TABLA 1: assets
    #Catalogo de los activos que vamos a trackear
    #--------------------------------
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='assets' AND xtype='U')
        CREATE TABLE assets (
            id          INT IDENTITY(1,1) PRIMARY KEY,   
            symbol      NVARCHAR(20) NOT NULL UNIQUE,     
            name        NVARCHAR(200) NOT NULL,             
            category    NVARCHAR(50) NOT NULL,             
            currency    NVARCHAR(50) DEFAULT 'USD',
            active      INT DEFAULT 1,        
            created_at  DATETIME DEFAULT GETDATE()
        )
    """)
    
    # -------------------------------------
    #   TABLA 2: price_history
    #   Cada fila = un precio capturado en un momento
    # -------------------------------------
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='price_history' AND xtype='U')
        CREATE TABLE price_history (
            id              INT IDENTITY(1,1) PRIMARY KEY,
            asset_id        INT NOT NULL,
            price           FLOAT NOT NULL,
            open_price      FLOAT,
            high_price      FLOAT,
            low_price       FLOAT,
            volume          BIGINT,
            change_pct      FLOAT,
            source          NVARCHAR(50) DEFAULT 'yfinance',
            scraped_at      DATETIME DEFAULT GETDATE(),
            FOREIGN KEY (asset_id) REFERENCES assets(id)
        )
    """)
    
    # -------------------------------------
    #   TABLA 3: scrape_logs
    #   Registro de cada corrida del scraper
    # -------------------------------------
    cursor.execute("""
        IF NOT EXISTS (SELECT * FROM sysobjects WHERE name='scrape_logs' AND xtype='U')
        CREATE TABLE scrape_logs (
            id          INT IDENTITY(1,1) PRIMARY KEY,
            status      NVARCHAR(20) NOT NULL,
            assets_ok   INTEGER DEFAULT 0,
            assets_fail INTEGER DEFAULT 0,
            message     NVARCHAR(500),
            ran_at      DATETIME DEFAULT GETDATE()
        )
    """)
    
    conn.commit()
    conn.close()
    print("Data base has been initialized correctly")
    
if __name__ == "__main__":
    create_database()
    init_db()


