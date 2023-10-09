import pandas as pd
import os
from scipy import stats
import numpy as np

def handle_missing_data(df):
    # Drop rows where all elements are missing
    df.dropna(how='all', inplace=True)
    
    # For each numeric column, fill missing values with the median of the column
    for col in df.select_dtypes(include=[np.number]).columns:
        df[col].fillna(df[col].median(), inplace=True)

def treat_outliers(df):
    # If we decide to treat outliers, we can implement the code here
    pass

def create_domain_specific_features(df):
    # Moving Averages
    df['7_day_MA'] = df['Close'].rolling(window=7).mean()
    df['21_day_MA'] = df['Close'].rolling(window=21).mean()
    
    # MACD
    df['12_day_EMA'] = df['Close'].ewm(span=12, adjust=False).mean()
    df['26_day_EMA'] = df['Close'].ewm(span=26, adjust=False).mean()
    df['MACD'] = df['12_day_EMA'] - df['26_day_EMA']
    
    # RSI
    delta = df['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    df['RSI'] = 100 - (100 / (1 + rs))
    
    # ROC
    df['ROC'] = df['Close'].pct_change(periods=9)
    
    # Bollinger Bands
    df['20_day_SMA'] = df['Close'].rolling(window=20).mean()
    df['20_day_STD'] = df['Close'].rolling(window=20).std()
    df['Upper_Bollinger'] = df['20_day_SMA'] + (df['20_day_STD'] * 2)
    df['Lower_Bollinger'] = df['20_day_SMA'] - (df['20_day_STD'] * 2)
    
    # Volatility
    df['Volatility'] = df['Close'].rolling(window=7).std()
    
    # Skewness and Kurtosis
    df['Skewness'] = df['Close'].rolling(window=21).apply(lambda x: stats.skew(x))
    df['Kurtosis'] = df['Close'].rolling(window=21).apply(lambda x: stats.kurtosis(x))
    
    return df

def main():
    # Directory where raw data is stored
    raw_data_dir = './data/raw/'

    # Directory where cleaned data will be stored
    cleaned_data_dir = './data/processed/'

    # Create directory if it doesn't exist
    if not os.path.exists(cleaned_data_dir):
        os.makedirs(cleaned_data_dir)

    # List all raw data files
    raw_data_files = os.listdir(raw_data_dir)

    for file in raw_data_files:
        print(f"Processing {file}...")
        
        # Load the raw data
        raw_data_path = os.path.join(raw_data_dir, file)
        df = pd.read_csv(raw_data_path)

        # Handle missing data
        handle_missing_data(df)
        
        # Treat outliers
        treat_outliers(df)
        
        # Create domain-specific features
        df = create_domain_specific_features(df)
        
        # Save cleaned and feature-engineered data
        cleaned_data_path = os.path.join(cleaned_data_dir, file)
        df.to_csv(cleaned_data_path, index=False)
        
        print(f"Finished processing {file}")

if __name__ == '__main__':
    main()
