"""
setup.py — Corre este archivo UNA SOLA VEZ para inicializar el proyecto.
Crea la base de datos SQLite y carga los 15 activos.
 
Uso:
    python setup.py
"""

import sys
import os

#Make sure python finds the project modules
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from database.db import create_database, init_db
from database.models import seed_assets

if __name__ == "__main__":
    print("Initializing Market Price Tracker...")
    print()
    
    print("Step 1: Creating SQL Server database...")
    create_database()

    print("Step 2: Creating tables...")
    init_db()
    
    print("Step 3: Loading asset catalog...")
    seed_assets()
    print()
    print("Setup complete. You can now run the scraper.")
    print("  Database: market_tracker")