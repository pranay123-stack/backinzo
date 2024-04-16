# for CE , otm = atm+ points , for itm = atm -points ,for PE  itm = atm+ points , for otm = atm -points ,


import pandas as pd
import re

def extract_expiry(ticker):
    match = re.search(r'(\d{2}[A-Z]{3}\d{2})', ticker)
    return match.group(0) if match else None

def sell_option(symbol, expiry, option_type, close_price, lot_size, amount_to_trade):
    num_lots = amount_to_trade // lot_size
    trade_value = num_lots * lot_size * close_price
    return f"Sold {num_lots} lots of {symbol} {option_type} at {close_price} expiring on {expiry}, total value {trade_value}"



def buy_option(symbol, expiry, option_type, close_price, lot_size, amount_to_trade):
    num_lots = amount_to_trade // lot_size
    trade_value = num_lots * lot_size * close_price
    return f"Bought {num_lots} lots of {symbol} {option_type} at {close_price} expiring on {expiry}, total value {trade_value}"


def strangle_backtest(csv_file_path, specific_time,sell_or_buy_ce,sell_or_buy_pe,points_ce,points_pe, add_or_minus_ce,add_or_minus_pe):
    df = pd.read_csv(csv_file_path)
    df['DateTime'] = pd.to_datetime(df['DateTime'])
    df = df[df['DateTime'].dt.time == pd.to_datetime(specific_time).time()]

    lot_size = 75  # Example lot size
    amount_to_trade = 150  # Example amount

    results = pd.DataFrame(columns=['DateTime', 'Ticker', 'Option Type', 'Adjusted ATM', 'Close Price', 'Trade Confirmation'])

    for index, row in df.iterrows():
        atm_price = row['ATM']
        adjusted_atm_ce = atm_price + points_ce if add_or_minus_ce else atm_price - points_ce
        adjusted_atm_pe = atm_price + points_pe if add_or_minus_pe else atm_price - points_pe
 
        nearest_strike_ce = (adjusted_atm_ce // 50) * 50 + (50 if adjusted_atm_ce % 50 >= 25 else 0)
        nearest_strike_pe = (adjusted_atm_pe // 50) * 50 + (50 if adjusted_atm_pe % 50 >= 25 else 0)

          # Construct Ticker names for CE and PE based on the nearest strike
        ticker_ce = f"{row['Ticker']}{nearest_strike_ce}CE"
        ticker_pe = f"{row['Ticker']}{nearest_strike_pe}PE"

        # Find the rows for CE and PE tickers at the nearest strike
        ce_row = df[(df['Ticker'] == ticker_ce) & (df['DateTime'] == specific_time)]
        pe_row = df[(df['Ticker'] == ticker_pe) & (df['DateTime'] == specific_time)]

        if not ce_row.empty and not pe_row.empty:
            ce_close = ce_row.iloc[0]['Close']
            pe_close = pe_row.iloc[0]['Close']
             # Extract expiry from ticker
            expiry = extract_expiry(row['Ticker'])

            if sell_or_buy_ce ==True:
                ce_trade_confirmation = sell_option(ticker_ce,expiry, 'CE', ce_close, lot_size, amount_to_trade)
                
            
            if sell_or_buy_pe == True:
                ce_trade_confirmation = sell_option(ticker_ce,expiry, 'PE', ce_close, lot_size, amount_to_trade)

            
            if sell_or_buy_pe == False:
                pe_trade_confirmation = buy_option(ticker_pe,expiry, 'PE', pe_close, lot_size, amount_to_trade)


            if sell_or_buy_ce == False:
                ce_trade_confirmation = buy_option(ticker_ce,expiry, 'CE', ce_close, lot_size, amount_to_trade)






            # Simulate selling CE and PE

  

   
    return ce_trade_confirmation, pe_trade_confirmation

# Configuration and execution
csv_file_path = 'path_to_your_data.csv'
specific_time = "09:20:59"
points_ce = 50  # Example points to adjust
points_pe = 50 # Example
option_type = 'CE'  # Could be 'CE' or 'PE'
add_or_minus_ce = True  # True to add points, False to subtract
add_or_minus_pe = True  # True to add points, False to subtract
sell_or_buy_ce = True  # True to sell, False to buy
sell_or_buy_pe = True  # True to sell, False to buy

# Run the backtest
result = strangle_backtest(csv_file_path, specific_time,sell_or_buy_ce,sell_or_buy_pe, points_ce,points_pe, add_or_minus_ce,add_or_minus_pe)
print(result)
