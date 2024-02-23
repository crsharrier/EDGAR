import requests 
import pandas as pd
from bs4 import BeautifulSoup
from datetime import datetime, timedelta
from yahoofinancials import YahooFinancials 
from typing import Union
import json
import os

# request headers: ========================================
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

# urls: ===================================================
dividendmax_pages = [
        r"https://www.dividendmax.com/market-index-constituents/s-and-p-100",
        r"https://www.dividendmax.com/market-index-constituents/s-and-p-100?page=2",
        r"https://www.dividendmax.com/market-index-constituents/s-and-p-100?page=3",
        r"https://www.dividendmax.com/market-index-constituents/s-and-p-100?page=4"
    ]
ticker_txt_url = r"https://www.sec.gov/include/ticker.txt"

# paths: ==================================================
sp100_html_path = r"edgar\requests_cache\sp100_page.html"
sp100_csv_path = r"edgar\requests_cache\sp100_tickers.csv"

ticker_cik_txt_path = r"edgar\requests_cache\ticker.txt"
ticker_cik_csv_path = r"edgar\requests_cache\ticker_cik.csv"
# ===============================================================================
# get_sp100()
# ===============================================================================

# Scrape across four pages from dividendmax.com which contain 
# tables of all sp100 entities and their tickers. Save to sp100_html_path
def request_sp100_html() -> bool:
    html_content = ''
    for url in dividendmax_pages:
        response = requests.get(url, headers=headers)
        if response.status_code != 200:
            print(f"request_sp100_html(): Failed to retrieve the HTML. Status code: {response.status_code}")
            return False
        html_content += response.content.decode('utf-8')
    
    with open(sp100_html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)
    return True


def parse_sp100_html(sp100_html: str) -> list:
    soup = BeautifulSoup(sp100_html, 'html.parser')
    tr_elements = soup.find_all('tr', class_='mdc-data-table__row')
    entity_names = \
        [tr.find_all('td', class_='mdc-data-table__cell')[0]\
         .get_text(strip=True) for tr in tr_elements]
    tickers = \
        [tr.find_all('td', class_='mdc-data-table__cell')[1]\
         .get_text(strip=True) for tr in tr_elements]

    df_row_list = []
    for name, ticker in zip(entity_names, tickers):
        df_row_list.append(
            {'entity_name': name,
             'ticker': ticker}
        )

    return df_row_list

# Return {ticker: entity_name} dict detailing current S&P 100.
# Scraped from across four pages on dividendmax.com
def get_sp100(force_download=False) -> pd.DataFrame:
    # load local file if exists:
    if not force_download:
        if os.path.exists(sp100_csv_path):
            try:
                df = pd.read_csv(sp100_csv_path)
                return df
            except:
                pass

    if not request_sp100_html():
        raise Exception("get_sp100(): Error obtaining sp100_html")
        
    with open(sp100_html_path, 'r') as f:
        sp100_html = f.read()
    
    df_row_list = parse_sp100_html(sp100_html)

    df = pd.DataFrame(df_row_list)
    try:
        df.to_csv(sp100_csv_path)
    except PermissionError:
        print(f"Unable to save {sp100_csv_path}. Is it being used by another program? (Excel?)")

    return df

# ===============================================================================
# get_ticker_cik_df()
# ===============================================================================
# Get txt from ticket_txt_url. Return success status.
def request_ticker_cik_txt() -> bool:
    response = requests.get(ticker_txt_url, headers=headers)
    if response.status_code != 200:
        print(f"request_cik_ticker_txt(): Failed to retrieve the HTML. Status code: {response.status_code}")
        return False

    txt_content = response.content

    with open(ticker_cik_txt_path, 'w', encoding='utf-8') as f:
        f.write(txt_content.decode('utf-8'))
    return True

def parse_ticker_cik_txt(txt_content: str) -> list:
    rows = []
    ticker = ''
    cik = ''
    append_to_cik = False
    for char in txt_content:
        if char == '\t':
            append_to_cik = True
            continue
        if char == '\n':
            rows.append({'ticker': ticker, 'cik': cik})
            ticker = ''
            cik = ''
            append_to_cik = False
            continue
        if append_to_cik:
            cik += char
        else:
            ticker += char
    return rows

def get_ticker_cik(force_download=False) -> pd.DataFrame:  
    if not request_ticker_cik_txt():
        raise Exception("get_ticker_cik(): Error obtaining ticker_cik_txt")
    
    with open(ticker_cik_txt_path, 'r', encoding='utf-8') as f:
        content = f.read()

    df_row_list = parse_ticker_cik_txt(content)

    df = pd.DataFrame(df_row_list)
    try:
        df.to_csv(ticker_cik_csv_path)
    except PermissionError:
        print(f"Unable to save {ticker_cik_csv_path}. Is it being used by another program? (Excel?)")

    return df

# Take ticker_cik_txt_path and return df containing ticker and cik.
# def get_ticker_cik_df(ticker_cik_txt_path: str, force_download=False) -> pd.DataFrame:
#     if not force_download:
#         if os.path.exists(ticker_cik_csv_path):
#             try:
#                 df = pd.read_csv(ticker_cik_csv_path)
#                 return df
#             except:
#                 pass

#     df = pd.DataFrame(cik_df_rows)
#     try:
#         df.to_csv(cik_csv_path)
#     except PermissionError:
#         print(f"Unable to save {cik_csv_path}. Is it being used by another program? (Excel?)")

#     return df

# Take cik_df containing entity_name and cik; and sp100_ticker_df
# containing entity_name and ticker. Assign each row in cik_df a ticker.
# Each ticker may correspond to multiple entities in cik_df
# Return df, stripped of non-sp100 entities.
# def add_ticker_to_cik_df(cik_df: pd.DataFrame) -> pd.DataFrame:
#     pass


# # Check if cik_lookup txt is already downloaded. If not, request it.
# # Return df containing entity_name, cik and ticker.
# def get_cik_df() -> dict:
#     if not os.path.exists(cik_txt_path):
#         if not request_cik_lookup_txt():
#             raise Exception("get_cik_lookup_dict(): Error obtaining cik_lookup_txt")
#     with open(cik_txt_path, 'r') as f:
#         cik_raw_txt = f.read()

#     cik_df = get_entity_cik_df(cik_raw_txt)

    # print(sp100_ticker_df.head())
    # print(cik_df.head())

    # merged_df = pd.merge(
    #     cik_df[cik_df['entity_name']
    #            .apply(lambda x: any(name in x for name in sp100_ticker_df['entity_name']))],
    #     sp100_ticker_df,
    #     on='entity_name',
    #     how='inner'
    #     )

    return cik_df

# ===============================================================================
# get_yahoo_data()
# ===============================================================================

# Add a certain number of days to date string. Return date string
def add_to_date_string(days: int, date: str) -> str:
    original_datetime = datetime.strptime(date, "%Y-%m-%d")
    new_datetime = original_datetime + timedelta(days=days)
    new_date_string = new_datetime.strftime("%Y-%m-%d")

    return new_date_string

# Take a 'price' dataframe and return the value of 'price' x days 
# in the future from a given date. 
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

# Take a historical_data dict and return a DataFrame containing 
# all relevant data for a certain ticker. Columns include:
# date, high, low, price, volume, symbol 
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

# Return DataFrame containing historical price data for provided tickers. 
def get_yahoo_data(start_date: str, 
                   end_date: str, 
                   tickers: Union[str, list[str]],
                   frequency: str='daily') -> pd.DataFrame:
    if isinstance(tickers, str):
        tickers = [tickers]

    data = YahooFinancials(tickers)
    historical_data = data.get_historical_price_data(
        start_date, end_date, frequency
        )
    # DEBUGGING:
    with open('historical_data.json', 'w') as f:
        json.dump(historical_data, f)
    column_names = ['date', 'high', 'low', 'price', 'volume',
                    '1daily_return', '2daily_return', '3daily_return', 
                    '5daily_return', '10daily_return', 'symbol']
    df = pd.DataFrame(columns=column_names)
    for ticker in tickers:
        new_df = get_data_for_ticker(ticker, historical_data)
        df = pd.concat([df, new_df], ignore_index=True, axis=0)

    return df

# ===============================================================================
# get_sentiment_word_dict()
# ===============================================================================

# Return a dictionary containing the LM sentiment words.
# The keys for the dictionary are the sentiments, 
# and the values will be a list of words associated with that particular sentiment.
def get_sentiment_word_dict():
    csv_path = r"data\Loughran-McDonald_MasterDictionary_1993-2021.csv"
    df = pd.read_csv(csv_path)

    columns = ['Negative', 'Positive', 'Uncertainty', 'Litigious', 
               'Strong_Modal', 'Weak_Modal', 'Constraining']
    sentiment_dict = {category: [] for category in columns}
    for category in columns:
        index_list = df[df[category] != 0].index
        for idx in index_list:
            word = df.iloc[idx, df.columns.get_loc('Word')]
            sentiment_dict[category].append(word)

    # DEBUGGING:
    # total_words = 0
    # for category in sentiment_dict.keys():
    #     num_words = len(sentiment_dict[category])
    #     print(f"{category} has {num_words} words")
    #     total_words += num_words
    # print(f"Total = {total_words} words")

    return sentiment_dict