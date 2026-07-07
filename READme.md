##### &#x09;**📈 Market Price Tracker**



A fully automated financial data pipeline that tracks real-time prices 

for 15 assets across Stocks, Crypto, Commodities and ETFs — 

built as a production-ready data service for fintech applications.



\---



###### **🚀 What problem does this solve?**



Financial teams and fintech startups spend hours manually checking 

market prices across multiple platforms. This system automates the 

entire process — collecting, storing, and visualizing real-time 

market data 24/7 without human intervention.



\---



###### **⚙️ How it works**

###### 

###### **📊 Assets Tracked (15 total)**



| Category | Assets |

|---|---|

| Stocks | AAPL, MSFT, GOOGL, TSLA, NVDA |

| Crypto | BTC-USD, ETH-USD, SOL-USD |

| Commodities | Gold, Crude Oil, Silver |

| ETFs | SPY, QQQ, VTI, GLD |



\---



###### 🛠️ **Tech Stack**



| Layer | Technology |

|---|---|

| Data Collection | Python, yfinance |

| Database | SQL Server |

| Automation | APScheduler |

| Dashboard | Streamlit, Plotly |

| ORM | SQLAlchemy, pyodbc |



\---



###### 📁 **Project Structure**



market-price-tracker/

│

├── scraper/

│   └── scraper.py          # Fetches live prices for all 15 assets

│

├── database/

│   ├── db.py               # SQL Server connection and table creation

│   └── models.py           # Asset catalog and data access functions

│

├── pipeline/

│   └── scheduler.py        # Runs scraper automatically every hour

│

├── analysis/

│   └── create\_views.py     # 5 SQL Server views for financial analysis

│

├── dashboard/

│   └── app.py              # Interactive Streamlit dashboard

│

├── setup.py                # One-command project initialization

├── requirements.txt

└── README.md



\---



###### **🗄️ Database Views**



| View | Purpose |

|---|---|

| `vw\_latest\_prices` | Current price for every asset |

| `vw\_best\_worst` | Best and worst performer today |

| `vw\_7day\_summary` | Weekly stats per asset |

| `vw\_most\_volatile` | Volatility ranking |

| `vw\_scraper\_health` | Scraper run history and status |



\---



###### **🚀 Getting Started**



1\. Install dependencies

&#x09;```bash

&#x09;	pip install -r requirements.txt

&#x09;	```



2\. Configure your SQL Server connection

&#x09;Edit `database/db.py` and update:

&#x09;	```python

&#x09;		SERVER   = 'YOUR\_SERVER\_NAME'

&#x09;		DATABASE = 'market\_tracker'

&#x09;		```



3\. Initialize the database

&#x09;```bash

&#x09;	python setup.py

&#x09;	```



4\. Run the scraper once

&#x09;```bash

&#x09;	python scraper/scraper.py

&#x09;	```



5\. Start the automated scheduler

&#x09;```bash

&#x09;	python pipeline/scheduler.py

&#x09;	```



6\. Launch the dashboard

&#x09;```bash

&#x09;	streamlit run dashboard/app.py

&#x09;	```

\---



**📬 Contact**



Built by Gibram Castellon — Accountant \& Data Scraping Developer  

Specializing in financial data automation.  

Available for freelance projects on Upwork.









