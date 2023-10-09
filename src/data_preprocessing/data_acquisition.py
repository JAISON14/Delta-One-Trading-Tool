import yfinance as yf
import os

def download_financial_data(asset_type, tickers, start_date='2022-01-01', end_date='2023-01-01'):
    """Download financial data for a list of tickers and save as CSV files."""
    
    raw_data_dir = './data/raw/'
    if not os.path.exists(raw_data_dir):
        os.makedirs(raw_data_dir)
    
    financial_data = {}
    
    for ticker in tickers:
        print(f"Downloading data for {ticker}...")
        financial_data[ticker] = yf.download(ticker, start=start_date, end=end_date)
        
        # Save the data to a CSV file in the raw data directory
        file_path = os.path.join(raw_data_dir, f"{asset_type}_{ticker}.csv")
        financial_data[ticker].to_csv(file_path)
    
    print("Data acquisition complete.")
    return financial_data


def main():
    assets = {
        'stocks': ['FB', 'AAPL', 'AMZN', 'NFLX', 'GOOGL'],  # FAANG stocks
        'etfs': ['SPY', 'QQQ'],
        'indices': ['^GSPC', '^IXIC']
    }
    
    all_financial_data = {}
    
    for asset_type, tickers in assets.items():
        all_financial_data[asset_type] = download_financial_data(asset_type, tickers)
    
if __name__ == '__main__':
    main()
