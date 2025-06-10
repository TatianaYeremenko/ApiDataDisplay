Both projects demonstrate end-to-end api data ingestion, transformation with pandas, and
rich interactive visualization (Plotly or Matplotlib)

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


