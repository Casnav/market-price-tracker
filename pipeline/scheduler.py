import os
import sys
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime
from scraper.scraper import run_scraper

# -----------------------------------------------
# CONFIG
# -----------------------------------------------
RUN_EVERY_HOURS = 0.03 # May this we can change as we wish

scheduler = BlockingScheduler()

def scheduled_job():
    print(f"\n[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] Running scheduled scrape...")
    try:
        run_scraper()
    except Exception as e:
        print(f"Scheduler job failed: {e}")

if __name__ == "__main__":
    print("=" * 50)
    print(" Market Price Tracker - Scheduler started")
    print(f"    Job will run every {RUN_EVERY_HOURS} hour(s)")
    print("    Press CTRL+C to stop")
    print("=" * 50)
    
    #   Run once immediately on startup, then on the interval
    scheduled_job()
    
    scheduler.add_job(scheduled_job,'interval', hours=RUN_EVERY_HOURS)
    
    try:
        scheduler.start()
    except (KeyboardInterrupt, SystemExit):
        print("\nScheduler stopped.")