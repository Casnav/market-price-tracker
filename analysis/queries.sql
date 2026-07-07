-- VIEW 1: Lastest price per asset
CREATE VIEW IF NOT EXISTS vw_latest_prices AS
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
);

-- VIEW 2: Best and worst performer today
CREATE VIEW IF NOT EXISTS vw_best_worst AS
SELECT symbol, name, price, change_pct,
	CASE
		WHEN change_pct = (SELECT MAX(change_pct) FROM vw_latest_prices) THEN 'Best'
		WHEN change_pct = (SELECT MIN(change_pct) FROM vw_latest_prices) THEN 'Worst'
	END as performance
FROM vw_latest_prices
WHERE change_pct = (SELECT MAX(change_pct) FROM vw_latest_prices)
	OR change_pct = (SELECT MIN(change_pct) FROM vw_latest_prices);

-- VIEW 3: Price summary per asset (7 day stats)
CREATE VIEW IF NOT EXISTS vw_7day_summary AS
SELECT
	a.symbol,
	a.name,
	a.category,
	ROUND(AVG(p.price), 2) as avg_price,
	ROUND(MAX(p.price), 2) as max_price,
	ROUND(MIN(p.price), 2) as min_price,
	ROUND(MAX(p.price) - MIN(p.price), 2) as price_range,
	COUNT(*) as data_points
FROM assets a
INNER JOIN price_history p ON a.id = p.asset_id
WHERE p.scraped_at >= datetime('now', '-7 days')
GROUP BY a.id, a.symbol, a.name, a.category;

-- VIEW 4: Scraper health log
CREATE VIEW IF NOT EXISTS vw_scraper_health AS
SELECT
	status,
	assets_ok,
	assets_fail,
	message,
	ran_at,
FROM scrape_logs
ORDER BY ran_at DESC;