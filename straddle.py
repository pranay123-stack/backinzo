import pandas as pd
import re

def extract_expiry(ticker):
    """
    Extracts the expiry date from a ticker string using regex.
    
    Parameters:
    ticker (str): The ticker symbol from which to extract the expiry.
    
    Returns:
    str: The extracted expiry date.
    """
    match = re.search(r'(\d{2}[A-Z]{3}\d{2})', ticker)
    return match.group(0) if match else None

def sell_option(symbol, expiry, option_type, close_price, lot_size, amount_to_trade):
    """
    Simulates selling an option.
    
    Parameters:
    symbol (str): The ticker symbol for the option.
    expiry (str): Expiry date of the option.
    option_type (str): Type of option ('CE' for call, 'PE' for put).
    close_price (float): Price at which the option is being sold.
    lot_size (int): Number of units in one lot.
    amount_to_trade (int): Total number of units to trade.
    
    Returns:
    str: Confirmation message of the trade.
    """
    num_lots = amount_to_trade // lot_size
    trade_value = num_lots * lot_size * close_price
    return f"Sold {num_lots} lots of {symbol} {option_type} at {close_price} expiring on {expiry}, total value {trade_value}"


def straddle_backtest(csv_file_path, specific_time):
    # Load the CSV file with market data
    df = pd.read_csv(csv_file_path)
    
    # Convert 'DateTime' to datetime object and filter data for the specific time
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df = df[df['DateTime'].dt.time == pd.to_datetime(specific_time).time()]

      # Assuming a generic lot size and amount to trade for simplicity
    lot_size = 15  # Common lot size for Nifty options
    amount_to_trade = 15000  # Example amount, adjust as needed


    # Results DataFrame to store outcomes of each trade
    results = pd.DataFrame(columns=['DateTime', 'Ticker CE', 'Ticker PE', 'CE Close Price', 'PE Close Price', 'CE Sell Order', 'PE Sell Order', 'Total Profit'])

    for index, row in df.iterrows():
        atm_price = row['ATM']
        nearest_strike = (atm_price // 50) * 50 + (50 if atm_price % 50 >= 25 else 0)

        # Construct Ticker names for CE and PE based on the nearest strike
        ticker_ce = f"{row['Ticker']}{nearest_strike}CE"
        ticker_pe = f"{row['Ticker']}{nearest_strike}PE"

        # Find the rows for CE and PE tickers at the nearest strike
        ce_row = df[(df['Ticker'] == ticker_ce) & (df['DateTime'] == specific_time)]
        pe_row = df[(df['Ticker'] == ticker_pe) & (df['DateTime'] == specific_time)]

        if not ce_row.empty and not pe_row.empty:
            ce_close = ce_row.iloc[0]['Close']
            pe_close = pe_row.iloc[0]['Close']
             # Extract expiry from ticker
            expiry = extract_expiry(row['Ticker'])


            # Simulate selling CE and PE
            ce_trade_confirmation = sell_option(ticker_ce,expiry, 'CE', ce_close, lot_size, amount_to_trade)
            pe_trade_confirmation = sell_option(ticker_pe,expiry, 'PE', pe_close, lot_size, amount_to_trade)







          
    return ce_trade_confirmation, pe_trade_confirmation

# File path setup
csv_file_path = 'path_to_your_data.csv'
specific_time = "09:20:59"  # Set the specific time for analysis

# Execute the straddle backtest at the specific time
result = straddle_backtest(csv_file_path, specific_time)
print(result)
