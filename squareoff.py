import pandas as pd
from datetime import datetime

def square_off_premium(file_path, symbol, strike_price, option_type, expiry,side ,premium_value, threshold_pct, start_time_str, end_time_str):
    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Ensure 'DateTime' column is in datetime format
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Convert string time to datetime.time and combine with date from DataFrame for full datetime
    start_time = datetime.combine(df['DateTime'].iloc[0].date(), datetime.strptime(start_time_str, "%H:%M:%S").time())
    end_time = datetime.combine(df['DateTime'].iloc[0].date(), datetime.strptime(end_time_str, "%H:%M:%S").time())

    # Filter the data for the specific symbol, option type, strike price, and expiry
    df_filtered = df[(df['Symbol'] == symbol) & 
                     (df['DateTime'] > start_time) & 
                     (df['DateTime'] <= end_time) & 
                     (df['Strike'] == strike_price) & 
                     (df['OptionType'] == option_type) & 
                     (df['Expiry'] == expiry)]

    # Determine entry price based on input
    entry_premium = premium_value

    for index, row in df_filtered.iterrows():
        current_premium = row['premium']

        if option_type == "CE":

            # Check conditions to square off
            if side == "buy" and current_premium <=  entry_premium * (1 - threshold_pct / 100):
                print(f"Square off Buy at {current_premium} at {row['DateTime']}")
                break
            elif side == "sell" and current_premium >=  entry_premium * (1 + threshold_pct / 100):
                print(f"Square off Sell at {current_premium} at {row['DateTime']}")
                break
        if option_type == "PE":

            # Check conditions to square off
            if side == "buy" and current_premium <=  entry_premium * (1 - threshold_pct / 100):
                print(f"Square off Buy at {current_premium} at {row['DateTime']}")
                break
            elif side == "sell" and current_premium >=  entry_premium * (1 + threshold_pct / 100):
                print(f"Square off Sell at {current_premium} at {row['DateTime']}")
                break


# File path to the CSV
file_path = 'path_to_your_csv.csv'

# Parameters for backtesting
symbol = 'AAPL'  # Example symbol/ticker
strike_price = 100  # Example strike price
option_type = 'Call'  # 'Call' or 'Put'
expiry = '2024-01-19'  # Example expiry date
premium_value_at_buy_or_sell = 10  # Premium value at the time of buy or sell
threshold_pct = 10  # Percentage threshold for squaring off
start_time_str = "09:15:59"  # Start time to check the premiums
end_time_str = "15:19:59"  # End time to check the premiums
side = "buy" # Side
# Execute the backtest
square_off_premium(file_path, symbol, strike_price, option_type, expiry,side, premium_value_at_buy_or_sell, threshold_pct, start_time_str, end_time_str)








def square_off_underlying(file_path, strikeprice_before_rounding_off,strikeprice_after_rounding_off,underlying_points,symbol, option_type, expiry, side, traded_price_of_strikeprice_after_rounding_off, threshold_pct, start_time_str, end_time_str):

    # Load the CSV file
    df = pd.read_csv(file_path)
    
    # Ensure 'DateTime' column is in datetime format
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Convert string time to datetime.time and combine with date from DataFrame for full datetime
    start_time = datetime.combine(df['DateTime'].iloc[0].date(), datetime.strptime(start_time_str, "%H:%M:%S").time())
    end_time = datetime.combine(df['DateTime'].iloc[0].date(), datetime.strptime(end_time_str, "%H:%M:%S").time())

    # Filter the data for the specific symbol, option type, strike price, and expiry
    df_filtered = df[(df['Symbol'] == symbol) & 
                     (df['DateTime'] > start_time) & 
                     (df['DateTime'] <= end_time) & 
                     (df['Strike'] ==  strikeprice_before_rounding_off) & 
                     (df['OptionType'] == option_type) & 
                     (df['Expiry'] == expiry)]

    # Loop through the filtered DataFrame
    for index, row in df_filtered.iterrows():
        current_option_price = row['optionPrice']

        if side == "buy":
            # Check conditions to square off for a Call
            if option_type == "CE" and  strikeprice_before_rounding_off>=  (underlying_points + strikeprice_before_rounding_off) :
                print(f"Square off Buy Call of {strikeprice_after_rounding_off} at {traded_price_of_strikeprice_after_rounding_off} at {row['DateTime']}")
                break
            # Check conditions to square off for a Put
            elif option_type == "PE" and current_option_price <=  (underlying_points + strikeprice_before_rounding_off):
                print(f"Square off Buy Put of {strikeprice_after_rounding_off} at {traded_price_of_strikeprice_after_rounding_off} at {row['DateTime']}")
                break
        elif side == "sell":
            # Check conditions to square off for a Call
            if option_type == "CE" and current_option_price >=   (underlying_points + strikeprice_before_rounding_off):
                print(f"Square off Sell Call of {strikeprice_after_rounding_off}at {traded_price_of_strikeprice_after_rounding_off} at {row['DateTime']}")
                break
            # Check conditions to square off for a Put
            elif option_type == "PE" and current_option_price <=  (underlying_points + strikeprice_before_rounding_off):
                print(f"Square off Sell Put of {strikeprice_after_rounding_off} at {traded_price_of_strikeprice_after_rounding_off} at {row['DateTime']}")
                break




# File path to the CSV
file_path = 'path_to_your_csv.csv'

# Parameters for backtesting
symbol = 'AAPL'  # Example symbol/ticker
strikeprice_before_rounding_off = 47880
strikeprice_after_rounding_off =47900
traded_price_of_strikeprice_after_rounding_off = 150  
option_type = 'CE'  # 'CE' for Call, 'PE' for Put
expiry = '2024-01-19'  # Example expiry date
threshold_pct = 10  # Percentage threshold for squaring off
start_time_str = "09:15:00"  # Start time to check the premiums
end_time_str = "15:19:59"  # End time to check the premiums
side = "buy" # Side (buy or sell)
underlying_points=100



# Execute the backtest
square_off_underlying(file_path, strikeprice_before_rounding_off,strikeprice_after_rounding_off,underlying_points,symbol, option_type, expiry, side, traded_price_of_strikeprice_after_rounding_off, threshold_pct, start_time_str, end_time_str)









import pandas as pd
from datetime import datetime, timedelta


def re_execute_trade(option_type,side):
            nonlocal entry_premium, current_time
            next_time_index = min(index + wait_time + 1, len(df_filtered) - 1)
            next_row = df_filtered.iloc[next_time_index]
            entry_premium = next_row['premium']  # New premium to enter at
            strike_price = next_row['ATM']  # New strike price assuming ATM
            current_time = next_row['DateTime']  # Update time
            
def squareoff_premium():
    pass



def square_off_premium_re_execute(file_path, symbol, option_type, expiry, side, threshold_pct, start_time_str, end_time_str, re_execute_times, wait_time):
    # Load the CSV file
    df = pd.read_csv(file_path)


    ce_total_execution = re_execute_times + entry_times
    pe_total_execution = re_execute_times + entry_times
    ce_reentry = 0
    pe_rentry =0


    
    # Ensure 'DateTime' column is in datetime format
    df['DateTime'] = pd.to_datetime(df['DateTime'])

    # Convert string times to datetime
    start_time = datetime.combine(df['DateTime'].iloc[0].date(), datetime.strptime(start_time_str, "%H:%M:%S").time())
    end_time = datetime.combine(df['DateTime'].iloc[0].date(), datetime.strptime(end_time_str, "%H:%M:%S").time())

    current_time = start_time
  

    while end_time != "15:20:59" and  ce_total_execution !=2 and pe_total_execution  !=2:
        # Filter the data for the specific symbol, option type, strike price, and expiry around current time
        df_filtered = df[(df['Symbol'] == symbol) & 
                         (df['DateTime'] >current_time) & 
                         (df['DateTime'] <= end_time) & 
                         (df['OptionType'] == option_type) & 
                         (df['Expiry'] == expiry)]
        
        if df_filtered.empty:
            break
        
        entry_premium = None

        for index, row in df_filtered.iterrows():
            current_premium = row['premium']
            current_time = row['DateTime']  # Update current time to row's time
            
            # Initialize entry premium if not set
            if entry_premium is None:
                entry_premium = current_premium

            # Define the re-execution condition inside each trade check
        
         
             
            if option_type == "CE":
                if side == "buy" and current_premium <= entry_premium * (1 - threshold_pct / 100):
                    print(f"Square off Buy at {current_premium} at {current_time}")
                    re_execute_trade(option_type,side)
                    continue
                elif side == "sell" and current_premium >= entry_premium * (1 + threshold_pct / 100):
                    print(f"Square off Sell at {current_premium} at {current_time}")
                    re_execute_trade(option_type,side)
                    continue

            if option_type == "PE":
                if side == "buy" and current_premium <= entry_premium * (1 - threshold_pct / 100):
                    print(f"Square off Buy at {current_premium} at {current_time}")
                    re_execute_trade(option_type,side)
                    continue
                elif side == "sell" and current_premium >= entry_premium * (1 + threshold_pct / 100):
                    print(f"Square off Sell at {current_premium} at {current_time}")
                    re_execute_trade(option_type,side)
                    continue

            if index == len(df_filtered) - 1:
                print("Reached the end of the available data within the given timeframe.")
                return

# File path to the CSV
file_path = 'path_to_your_csv.csv'
re_execute_times = 1
entry_times= 1

wait_time = 5

# Parameters for backtesting
symbol = 'AAPL'  # Example symbol/ticker
option_type = 'CE'  # 'CE' for Call, 'PE' for Put
expiry = '2024-01-19'  # Example expiry date
threshold_pct = 10  # Percentage threshold for squaring off
start_time_str = "09:15:59"  # Start time to check the premiums
end_time_str = "15:19:59"  # End time to check the premiums
side = "buy" # Side (buy or sell)

# Execute the backtest
square_off_premium_re_execute(file_path, symbol, option_type, expiry, side, threshold_pct, start_time_str, end_time_str, re_execute_times, wait_time)
