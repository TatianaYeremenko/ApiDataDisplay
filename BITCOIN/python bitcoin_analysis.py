import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo
from plotly.subplots import make_subplots

try:
    # Install and import CoinGecko API
    from pycoingecko import CoinGeckoAPI
    print("CoinGecko API imported successfully")
except ImportError:
    print("PyCoingecko not installed. Run: pip install pycoingecko")
    exit()

# Initialize CoinGecko API and fetch data
cg = CoinGeckoAPI()
print("Fetching Bitcoin price data for past 30 days...")
bitcoin_data = cg.get_coin_market_chart_by_id(id='bitcoin', vs_currency='usd', days=30)

# Convert to DataFrame
data = pd.DataFrame(bitcoin_data['prices'], columns=['TimeStamp', 'Price'])
data['Date'] = pd.to_datetime(data['TimeStamp'], unit='ms')

# Create candlestick data
candlestick_data = data.groupby(data.Date.dt.date).agg({
    'Price': ['min', 'max', 'first', 'last']
})
candlestick_data.columns = ['min', 'max', 'first', 'last']
candlestick_data.reset_index(inplace=True)

# Create subplots
fig = make_subplots(
    rows=2, cols=1,
    subplot_titles=('Bitcoin Candlestick Chart Over Past 30 Days', 'Bitcoin Price Trend - Past 30 Days'),
    vertical_spacing=0.1
)

# Add candlestick chart
fig.add_trace(
    go.Candlestick(
        x=candlestick_data.index,
        open=candlestick_data['first'],
        high=candlestick_data['max'],
        low=candlestick_data['min'],
        close=candlestick_data['last'],
        name='OHLC'
    ),
    row=1, col=1
)

# Add line chart
fig.add_trace(
    go.Scatter(
        x=data['Date'],
        y=data['Price'],
        mode='lines',
        name='Bitcoin Price',
        line=dict(color='orange', width=2)
    ),
    row=2, col=1
)

# Update layout
fig.update_layout(
    title='Bitcoin Analysis Dashboard - Past 30 Days',
    template='plotly_white',
    height=800,
    showlegend=True
)

fig.update_xaxes(title_text="Date", row=1, col=1, rangeslider_visible=False)
fig.update_xaxes(title_text="Date", row=2, col=1)
fig.update_yaxes(title_text="Price (USD $)", row=1, col=1)
fig.update_yaxes(title_text="Price (USD $)", row=2, col=1)

# Save combined chart
pyo.plot(fig, filename='bitcoin_combined_analysis.html', auto_open=False)
print("Combined chart saved as 'bitcoin_combined_analysis.html'")

# Display analysis
price_change = data['Price'].iloc[-1] - data['Price'].iloc[0]
price_change_pct = (price_change / data['Price'].iloc[0]) * 100
volatility = data['Price'].std()

print(f"\nPrice Analysis:")
print(f"   Starting price: ${data['Price'].iloc[0]:.2f}")
print(f"   Ending price: ${data['Price'].iloc[-1]:.2f}")
print(f"   Price change: ${price_change:.2f} ({price_change_pct:.2f}%)")
print(f"   Volatility (std): ${volatility:.2f}")

fig.show()