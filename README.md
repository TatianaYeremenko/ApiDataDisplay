## Bitcoin Price Analysis (BITCOIN folder)

This notebook (“Bitcoin Price Analysis with CoinGecko API”) fetches the last 30 days of
BTC/USD market data via the `pycoingecko` client, uses pandas to compute OHLC and summary
statistics, and then builds interactive Plotly candlestick and line charts that are
assembled into a standalone HTML dashboard.

- [bitcoin_analysis_notebook.ipynb](BITCOIN/bitcoin_analysis_notebook.ipynb)

## NBA API Analysis (NBADATA folder)

This analysis (“NBA API Analysis – Golden State Warriors vs Toronto Raptors”) uses
`nba_api` to pull team metadata and the last six months of game logs for franchises like
the Warriors and Raptors, computes win-loss records and scoring averages, then
visualizes overall and home/away performance in Matplotlib charts (and exports results
to CSV/HTML).

- [nba_api_notebook.ipynb](NBADATA/nba_api_notebook.ipynb)

These notebooks demonstrate end-to-end data ingestion, transformation with pandas, and
rich interactive visualization (Plotly or Matplotlib) to deliver clear, insight-driven
dashboards across financial, sports, and web data domains.

## Web Data Acquisition and Visualization (WEBDATA folder)

This collection of notebooks, labs, and reference PDFs showcases web-based data
ingestion and interactive visualization workflows. Topics include REST API access with
`requests`, HTML scraping with `BeautifulSoup` and pandas, and building interactive
dashboards with Plotly.

- [requests_python_notebook.ipynb](WEBDATA/requests_python_notebook.ipynb)
- [web_scraping_tutorial.ipynb](WEBDATA/web_scraping_tutorial.ipynb)
- [pandas_web_scraping_notebook.ipynb](WEBDATA/pandas_web_scraping_notebook.ipynb)
- [fancy_interactive_viz_notebook.ipynb](WEBDATA/fancy_interactive_viz_notebook.ipynb)
- [practice_project.ipynb](WEBDATA/practice_project.ipynb)

Raw datasets for scraping exercises are located in `WEBDATA/content` (e.g.,
`WEBDATA/content/ai_job_dataset.csv`).
