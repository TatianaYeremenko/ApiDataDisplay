import pandas as pd
import plotly.graph_objects as go
import plotly.offline as pyo

try:
    from pycoingecko import CoinGeckoAPI
    print("CoinGecko API imported successfully")
except ImportError:
    print("PyCoingecko not installed. Run: pip install pycoingecko")
    exit()

try:
    # Initialize CoinGecko API
    cg = CoinGeckoAPI()
    print("CoinGecko API initialized")

    # Get Bitcoin market chart data for past 30 days
    print("Fetching Bitcoin price data for past 30 days...")
    bitcoin_data = cg.get_coin_market_chart_by_id(
        id='bitcoin',
        vs_currency='usd',
        days=30
    )

    print(f"Successfully fetched Bitcoin data")
    print(f"Data keys: {list(bitcoin_data.keys())}")
    print(f"Price data points: {len(bitcoin_data['prices'])}")

except Exception as e:
    print(f"Error fetching data: {e}")
    exit()

try:
    # Convert price data to DataFrame
    data = pd.DataFrame(bitcoin_data['prices'], columns=['TimeStamp', 'Price'])
    print(f"Created DataFrame with shape: {data.shape}")

    # Convert timestamp to datetime
    data['Date'] = pd.to_datetime(data['TimeStamp'], unit='ms')
    print("Converted timestamps to datetime")

    # Display basic info
    print(f"\nData Info:")
    print(f"   Date range: {data['Date'].min()} to {data['Date'].max()}")
    print(f"   Price range: ${data['Price'].min():.2f} to ${data['Price'].max():.2f}")
    print(f"   Average price: ${data['Price'].mean():.2f}")

    # Show sample data
    print(f"\nSample data:")
    print(data[['Date', 'Price']].head())
except Exception as e:
    print(f"Error processing data: {e}")
    exit()

try:
    # Group by date to create OHLC (Open, High, Low, Close) data
    candlestick_data = data.groupby(data.Date.dt.date).agg({
        'Price': ['min', 'max', 'first', 'last']
    })

    # Flatten column names
    candlestick_data.columns = ['min', 'max', 'first', 'last']
    candlestick_data.reset_index(inplace=True)

    print(f"Candlestick data shape: {candlestick_data.shape}")
    print(f"Sample candlestick data:")
    print(candlestick_data.head())
except Exception as e:
    print(f"Error creating candlestick data: {e}")
    exit()

try:
    # Create candlestick chart using Plotly
    fig_candlestick = go.Figure(data=[go.Candlestick(
        x=candlestick_data.index,
        open=candlestick_data['first'],
        high=candlestick_data['max'],
        low=candlestick_data['min'],
        close=candlestick_data['last']
    )])

    # Update layout
    fig_candlestick.update_layout(
        xaxis_rangeslider_visible=False,
        xaxis_title='Date',
        yaxis_title='Price (USD $)',
        title='Bitcoin Candlestick Chart Over Past 30 Days',
        template='plotly_white'
    )

    print("Candlestick chart created successfully")

    # Save candlestick chart as HTML file
    pyo.plot(fig_candlestick, filename='bitcoin_candlestick_chart.html', auto_open=False)
    print("Chart saved as 'bitcoin_candlestick_chart.html'")

except Exception as e:
    print(f"Error creating candlestick chart: {e}")

try:
    # Create simple line chart
    fig_line = go.Figure()

    fig_line.add_trace(go.Scatter(
        x=data['Date'],
        y=data['Price'],
        mode='lines',
        name='Bitcoin Price',
        line=dict(color='orange', width=2)
    ))

    fig_line.update_layout(
        title='Bitcoin Price Trend - Past 30 Days',
        xaxis_title='Date',
        yaxis_title='Price (USD $)',
        template='plotly_white',
        hovermode='x unified'
    )

    # Save line chart
    pyo.plot(fig_line, filename='bitcoin_price_trend.html', auto_open=False)
    print("Price trend chart saved as 'bitcoin_price_trend.html'")

except Exception as e:
    print(f"Error creating line chart: {e}")

try:
    # Price statistics
    price_change = data['Price'].iloc[-1] - data['Price'].iloc[0]
    price_change_pct = (price_change / data['Price'].iloc[0]) * 100
    volatility = data['Price'].std()

    print(f"Price Analysis:")
    print(f"   Starting price: ${data['Price'].iloc[0]:.2f}")
    print(f"   Ending price: ${data['Price'].iloc[-1]:.2f}")
    print(f"   Price change: ${price_change:.2f} ({price_change_pct:.2f}%)")
    print(f"   Volatility (std): ${volatility:.2f}")

    # Daily price changes
    data['Daily_Change'] = data['Price'].pct_change() * 100
    daily_changes = data['Daily_Change'].dropna()

    print(f"\nDaily Change Analysis:")
    print(f"   Average daily change: {daily_changes.mean():.2f}%")
    print(f"   Max daily gain: {daily_changes.max():.2f}%")
    print(f"   Max daily loss: {daily_changes.min():.2f}%")
except Exception as e:
    print(f"Error in analysis: {e}")

# Create combined HTML page
try:
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Bitcoin Analysis Dashboard</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 20px; }}
            .chart-container {{ margin: 20px 0; }}
            .stats {{ background: #f5f5f5; padding: 15px; border-radius: 5px; margin: 20px 0; }}
        </style>
    </head>
    <body>
        <h1>Bitcoin Analysis Dashboard - Past 30 Days</h1>
        
        <div class="stats">
            <h3>Price Statistics</h3>
            <p><strong>Date Range:</strong> {data['Date'].min().strftime('%Y-%m-%d')} to {data['Date'].max().strftime('%Y-%m-%d')}</p>
            <p><strong>Starting Price:</strong> ${data['Price'].iloc[0]:.2f}</p>
            <p><strong>Ending Price:</strong> ${data['Price'].iloc[-1]:.2f}</p>
            <p><strong>Price Change:</strong> ${price_change:.2f} ({price_change_pct:.2f}%)</p>
            <p><strong>Volatility (std):</strong> ${volatility:.2f}</p>
        </div>
        
        <div class="chart-container">
            <h2>Candlestick Chart</h2>
            <iframe src="bitcoin_candlestick_chart.html" width="100%" height="600" frameborder="0"></iframe>
        </div>
        
        <div class="chart-container">
            <h2>Price Trend</h2>
            <iframe src="bitcoin_price_trend.html" width="100%" height="600" frameborder="0"></iframe>
        </div>
    </body>
    </html>
    """
    
    with open('bitcoin_combined_dashboard.html', 'w') as f:
        f.write(html_content)
    
    print("Combined dashboard saved as 'bitcoin_combined_dashboard.html'")
    
    # Open the combined dashboard in default browser
    import webbrowser
    import os
    
    dashboard_path = os.path.abspath('bitcoin_combined_dashboard.html')
    webbrowser.open(f'file://{dashboard_path}')
    print("Opening dashboard in browser...")
    
except Exception as e:
    print(f"Error creating combined dashboard: {e}")

print("\nScript completed. Dashboard should open in your browser automatically.")