import requests
import json
import pandas as pd
import os
import re
from edgar.ref_data import get_sp100, get_ticker_cik


headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}

company_search_url = r"https://www.sec.gov/edgar/searchedgar/companysearch"


# Take in the URL and write the html file to the path specified. 
# Return success status.
def write_page(url: str, file_path: str) -> bool:
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"write_page(): Failed to retrieve the HTML. Status code: {response.status_code}")
        return False
    html_content = response.content.decode('utf-8')

    with open(file_path, 'w', encoding='utf-8', newline='') as f:
        f.write(html_content)

    return True


def clean_ticker(ticker: str) -> str:
    stripped = re.sub(r'[^a-zA-Z]', '', ticker)
    return stripped.upper()
    

def get_ciks_from_ticker(ticker: str) -> pd.DataFrame:
    sp100_df = get_sp100()
    ticker_cik_df = get_ticker_cik()

    sp100_df['ticker'] = sp100_df['ticker'].apply(lambda x: clean_ticker(x))
    ticker_cik_df['ticker'] = ticker_cik_df['ticker'].apply(lambda x: clean_ticker(x))

    joined_df = pd.merge(sp100_df, ticker_cik_df, how='right', on='ticker')
    print(joined_df.head())
    print('len = ' + str(len(joined_df)))

    return joined_df.loc[joined_df['ticker'] == ticker]


# Download all the html 10-k files for the given ticker into the destination folder. 
# Name downloaded files according to the following convention:
# <ticker>_10-k_<filing_date>.html
# Return success status.
def download_files_10k(ticker: str, dest_folder: str) -> bool:
    df_rows = get_ciks_from_ticker(ticker)

    for index, row in df_rows.iterrows():
        cik = row['cik']
        ticker = row['ticker']
        url = r"https://www.sec.gov/edgar/browse/?CIK=" + cik + r"&owner=exclude"
        file_path = dest_folder + ticker + "_10-k_" + "date.html"
        write_page(url, file_path)
       
    return True
  
