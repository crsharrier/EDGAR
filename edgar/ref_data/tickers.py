from edgar.DataSource import DataSource
from bs4 import BeautifulSoup
import pandas as pd
import re
from edgar.constants import *

def parse_ticker_cik_txt(txt_content: str) -> pd.DataFrame:
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
    return pd.DataFrame(rows)

def parse_sp100_html(sp100_html: str) -> pd.DataFrame:
    soup = BeautifulSoup(sp100_html, 'html.parser')
    tr_elements = soup.find_all('tr', class_='mdc-data-table__row')
    entity_names = \
        [tr.find_all('td', class_='mdc-data-table__cell')[0]\
         .get_text(strip=True) for tr in tr_elements]
    tickers = \
        [tr.find_all('td', class_='mdc-data-table__cell')[1]\
         .get_text(strip=True) for tr in tr_elements]

    rows = []
    for name, ticker in zip(entity_names, tickers):
        rows.append(
            {'entity_name': name,
             'ticker': ticker}
        )

    df = pd.DataFrame(rows)
    return df

dividendmax_pages = [
        r"https://www.dividendmax.com/market-index-constituents/s-and-p-100",
        r"https://www.dividendmax.com/market-index-constituents/s-and-p-100?page=2",
        r"https://www.dividendmax.com/market-index-constituents/s-and-p-100?page=3",
        r"https://www.dividendmax.com/market-index-constituents/s-and-p-100?page=4"
    ]

sp100 = DataSource(dividendmax_pages,
                   parse_sp100_html,
                   RAW + r"sp100_page.html",
                   PROCESSED + r"sp100_tickers.csv")

ticker_cik = DataSource(r"https://www.sec.gov/include/ticker.txt",
                        parse_ticker_cik_txt,
                        RAW + r"ticker.txt",
                        PROCESSED + r"ticker_cik.csv")

def clean_ticker(ticker: str) -> str:
    stripped = re.sub(r'[^a-zA-Z]', '', ticker)
    return stripped.upper()
    
def get_sp100() -> dict:
    sp100_df = sp100.df
    ticker_cik_df = ticker_cik.df

    # clean the ticker column of each df
    sp100_df['ticker'] = sp100_df['ticker'].astype(str)
    sp100_df['ticker'] = sp100_df['ticker'].apply(lambda x: clean_ticker(x))
    ticker_cik_df['ticker'] = ticker_cik_df['ticker'].astype(str)
    ticker_cik_df['ticker'] = ticker_cik_df['ticker'].apply(lambda x: clean_ticker(x))

    joined_df = pd.merge(sp100_df, ticker_cik_df, how='right', on='ticker')
    joined_df = joined_df[joined_df['entity_name'].notnull()]

    sp100_dict = dict(zip(joined_df['ticker'], joined_df['cik']))
    
    return sp100_dict