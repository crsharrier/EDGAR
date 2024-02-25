import json
import pandas as pd
from tqdm import tqdm
from typing import Union
from datetime import datetime, timedelta
from yahoofinancials import YahooFinancials

'''
Add a certain number of days to date string. Return date string
'''
def add_to_date_string(days: int, date: str) -> str:
    original_datetime = datetime.strptime(date, "%Y-%m-%d")
    new_datetime = original_datetime + timedelta(days=days)
    new_date_string = new_datetime.strftime("%Y-%m-%d")

    return new_date_string

'''
Take a 'price' dataframe and return the value of 'price' x days 
in the future from a given date.
'''
def calculate_x_daily_return(df: pd.DataFrame,
                             days: int,  
                             date: str) -> int:
    future_date = add_to_date_string(days, date)
    
    # check rows exist before trying to access them
    price_row = df.loc[df['date'] == date, 'price']
    future_row = df.loc[df['date'] == future_date, 'price']

    # check for earlier dates
    while future_row.empty and days > 1:
        days -= 1
        future_date = add_to_date_string(days, date)
        future_row = df.loc[df['date'] == future_date, 'price']
    
    if future_row.empty:
        return None 

    price = price_row.values[0]
    future_price = future_row.values[0]
    return future_price - price

'''
Take a historical_data dict and return a DataFrame containing 
all relevant data for a certain ticker. Columns:
    [date, high, low, price, volume, symbol, (1, 2, 3, 5, 10)daily_return]
'''
def get_data_for_ticker(ticker: str,
                        historical_data: dict) -> pd.DataFrame:
    prices_list = historical_data[ticker]['prices']
    columns= ['formatted_date', 'high', 'low', 'volume', 'close']
    new_df = pd.DataFrame(prices_list)[columns]
    
    new_df = new_df.rename(columns={'formatted_date': 'date', 'close': 'price'})
    new_df['symbol'] = ticker

    for x in [1, 2, 3, 5, 10]:
        column_name = f"{x}daily_return"
        new_df[column_name] = new_df['date'].apply(
            lambda date: calculate_x_daily_return(new_df, x, date)
        ) 
                                            
    return new_df

'''
Return DataFrame containing historical price data for provided tickers.
'''
def get_yahoo_data(start_date: str, 
                   end_date: str, 
                   tickers: Union[str, list[str]],
                   frequency: str='daily') -> pd.DataFrame:
    if isinstance(tickers, str):
        tickers = [tickers]
    column_names = ['date', 'high', 'low', 'price', 'volume',
                    '1daily_return', '2daily_return', '3daily_return', 
                    '5daily_return', '10daily_return', 'symbol']
    df = pd.DataFrame(columns=column_names)

    with tqdm(total=len(tickers), desc="Processing tickers") as pbar:
        for ticker in tickers:
            try:
                data = YahooFinancials(ticker)
                historical_data = data.get_historical_price_data(
                    start_date, end_date, frequency
                    )
                new_df = get_data_for_ticker(ticker, historical_data)
                df = pd.concat([df, new_df], ignore_index=True, axis=0)
            except Exception as e:
                print(f"Error processing ticker {ticker}: {e}")
                continue
            finally:
                pbar.set_description(f" Getting historical data for: {ticker}")
                pbar.update(1)

    return df
