import sys
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from database.db import get_connection

VIEWS ={
    "vw_latest_prices":
        """
        CREATE VIEW vw_latest_prices AS
        SELECT
            a.symbol,
            a.name,
            a.category,
            p.price,
            p.high_price,
            p.low_price,
            p.volume,
            p.change_pct,
            p.scraped_at
        FROM assets a
        INNER JOIN price_history p ON a.id = p.asset_id
        WHERE p.scraped_at = (
            SELECT MAX(scraped_at)
            FROM price_history
            WHERE asset_id = a.id
        )
        """,
    
    "vw_best_worst":
        """
        CREATE VIEW vw_best_worst AS
        SELECT TOP 1 symbol, name, price, change_pct, 'Best' as performance
        FROM vw_latest_prices
        ORDER BY change_pct DESC
        
        UNION ALL
        
        SELECT TOP 1 symbol, name, price, change_pct, 'Worst' as performance
        FROM vw_latest_prices
        ORDER BY change_pct ASC
        """,
        
    "vw_7day_summary":
        """
        CREATE VIEW vw_7day_summary AS
        SELECT
            a.symbol,
            a.name,
            a.category,
            ROUND(AVG(p.price), 2)      as avg_price,
            ROUND(MAX(p.price), 2)      as max_price,
            ROUND(MIN(p.price), 2)      as min_price,
            ROUND(MAX(p.price) - MIN(p.price), 2) as price_range,
            COUNT(*)                    as data_points
        from assets a
        INNER JOIN price_history p ON a.id = p.asset_id
        WHERE p.scraped_at >= DATEADD(day,-7, GETDATE())
        GROUP BY a.symbol, a.name, a.category
        """,
        
    "vw_most_volatile":
        """
        CREATE VIEW vw_most_volatile AS
        SELECT
            symbol,
            name,
            category,
            max_price,
            min_price,
            price_range,
            ROUND(price_range * 100.0 / avg_price, 2) as volatility_pct
        FROM vw_7day_summary
        """,
        
    "vw_scraper_health":
        """
        CREATE VIEW vw_scraper_health AS
        SELECT
            status,
            assets_ok,
            assets_fail,
            message,
            ran_at
        FROM scrape_logs
        """ 
}

def drop_view(cursor, view_name):
    """Drops the view if it already exists."""
    cursor.execute(f"""
        IF EXISTS (SELECT * FROM sys.views WHERE name = '{view_name}')
        DROP VIEW {view_name}
    """)
    
def create_views():
    conn = get_connection()
    cursor = conn.cursor()
    
    for view_name, view_sql in VIEWS.items():
        try:
            drop_view(cursor, view_name)
            conn.commit()
            cursor.execute(view_sql)
            conn.commit()
            print(f"{view_name} created successfully.")
        except Exception as e:
            print(f"Error creating {view_name}: {e}")
    
    conn.close()
    print("\nAll views processed")
    
    
if __name__ == "__main__":
    create_views()