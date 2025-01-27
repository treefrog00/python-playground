import os
import json
import hashlib
from pathlib import Path
from functools import wraps
from datetime import datetime
import requests
import streamlit as st
import pandas as pd


def disk_cache():
    cache_path = Path('~/tmp/api_cache').expanduser()
    cache_path.mkdir(exist_ok=True)

    def decorator(func):
        @wraps(func)
        def wrapper(url):
            # Create a unique filename based on the URL
            url_hash = hashlib.md5(url.encode()).hexdigest()
            cache_file = cache_path / f"{url_hash}.json"

            if cache_file.exists():
                print("using cache")
                with open(cache_file) as f:
                    return json.load(f)

            result = func(url)

            with open(cache_file, 'w') as f:
                json.dump(result, f)

            return result
        return wrapper
    return decorator


@disk_cache()
def fetch_api_data(url):
    """Fetch data from API with caching"""
    r = requests.get(url)
    return r.json()


def main():
    st.title('Silly Streamlit + API intergration example, mostly written using aider.chat 🤖')

    api_key = os.environ.get('ALPHA_VANTAGE_API_KEY')
    if not api_key:
        st.error("Please set ALPHA_VANTAGE_API_KEY environment variable")
        return

    ibm_url = f'https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=IBM&apikey={api_key}'
    btc_market_trade_url = f'https://www.alphavantage.co/query?function=DIGITAL_CURRENCY_MONTHLY&symbol=DOGE&market=USD&apikey={api_key}'

    # Fetch and process IBM data
    ibm_data = fetch_api_data(ibm_url)["Monthly Time Series"]
    ibm_vals = [(datetime.strptime(timestamp, '%Y-%m-%d'), float(values["4. close"]))
                for timestamp, values in ibm_data.items()]

    # Fetch and process DOGE data
    doge_data = fetch_api_data(btc_market_trade_url)["Time Series (Digital Currency Monthly)"]
    doge_vals = [(datetime.strptime(timestamp, '%Y-%m-%d'), float(values["4. close"]))
                for timestamp, values in doge_data.items()]

    # Create DataFrames
    ibm_df = pd.DataFrame(ibm_vals, columns=['date', 'price']).sort_values('date')
    doge_df = pd.DataFrame(doge_vals, columns=['date', 'price']).sort_values('date')

    # Create plots
    st.subheader('IBM Stock Price')
    st.line_chart(ibm_df.set_index('date'))

    st.subheader('Doge Price')
    st.line_chart(doge_df.set_index('date'))


if __name__ == '__main__':
    main()
