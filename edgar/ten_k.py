import os
import io
import pandas as pd
from typing import Union, Optional
from bs4 import BeautifulSoup

from edgar.constants import *
from edgar.DataSource import DataSource
from edgar.ref_data.tickers import get_sp100


'''
DataSource parse method.
Returns Series called 'Period', containing name of year or qtr
'''
def parse_index_html(html: str) -> pd.DataFrame:
    soup = BeautifulSoup(html, 'html.parser')
    rows = soup.find_all('tr')

    data = []
    for row in rows:
        first_td = row.find('td')
        if first_td:
            a_tag = first_td.find('a')
            if a_tag:
                link = a_tag.text
                if link.isnumeric() or \
                    link in ['QTR1', 'QTR2', 'QTR3', 'QTR4']:
                    row = {'Period': link}
                    if row not in data:
                        data.append(row)
    return pd.DataFrame(data)

'''
DataSource parse method.
Return df of parsed company.idx file 
'''
def parse_idx(index_str: str) -> pd.DataFrame:
    names = ['Company Name','Form Type','CIK','Date Filed','File Name']
    fwf_file = io.StringIO(index_str)
    df = pd.read_fwf(fwf_file, 
                    colspecs=[(0,62),(62,74),(74,84),(86,96),(98,146)], 
                    names=names, 
                    skiprows=11)
    return df

class Index:
    '''
    Return df containing urls for company.idx files.
    Columns: [year, quarter, url]
    '''
    @property
    def urls(self) -> pd.Series:
        URLS_CSV = INDEX_PATH + "urls.csv"
        if os.path.isfile(URLS_CSV):
            print("Loading index urls from local file...")
            return pd.read_csv(URLS_CSV)
        
        print("Scraping index urls...")
        data = []
        full_index = DataSource(FULL_INDEX_URL, parse_index_html)
        years = list(full_index.df['Period'])
        #TODO: Add error check for years with no records
        for year in years:
            current = DataSource(FULL_INDEX_URL + year + '/', parse_index_html)
            qtrs = list(current.df['Period'])
            for qtr in qtrs:
                url = f"{FULL_INDEX_URL}{year}/{qtr}/company.idx"
                data.append({'Year': year, 'Quarter': qtr, 'URL': url})
        print(f"{len(data)} urls found.")

        df = pd.DataFrame(data)
        df.to_csv(URLS_CSV)

        return df   
    
    '''
    Return df containing all of the processed idx files.
    Columns: [Company Name, Form Type, CIK, Date FIled, File Name]
    '''
    def get_idx(self, 
                start_year: int, 
                end_year: Optional[int]=None) -> pd.DataFrame:
        if not end_year:
            end_year = start_year
        years = range(start_year, end_year + 1)
        df = pd.DataFrame()
        for year in years:
            urls = self.urls[self.urls['Year'] == year]
            for _, row in urls.iterrows():
                name = str(row['Year']) + '_' + str(row['Quarter'])
                print(f"Processing idx: {name}")
                idx = DataSource(row['URL'], parse_idx,
                                processed_path=INDEX_PATH + name + '.idx')
                df = pd.concat([df, idx.df.reset_index(drop=True)], ignore_index=True)
        return df

    
# example_index_url = r"https://www.sec.gov/Archives/edgar/full-index/2023/QTR4/company.idx"
# example_txt_url = "https://www.sec.gov/Archives/edgar/data/1084869/0001104659-13-008750.txt"

def parse_10k(html_text: str) -> str:
    soup = BeautifulSoup(html_text, 'html.parser')
    clean_text = soup.get_text(separator=' ', strip=True)
    return clean_text

sp100_dict = get_sp100()

'''
Download all the html 10-k files for the given ticker into the destination folder. 
Name downloaded files according to the following convention:
<ticker>_10-k_<filing_date>.html
Returns a list of DataSource objects, each representing a report.
'''
def download_files_10k(ticker: str, 
                       start_year: int, 
                       end_year: Optional[int]=None) -> list[DataSource]:
    if ticker not in sp100_dict:
        print(f'{ticker} not found in S&P100')
        return
    cik = sp100_dict[ticker]
    index = Index()
    idx = index.get_idx(start_year, end_year)
    subset_idx = idx[(idx['CIK'] == cik) & (idx['Form Type'] == '10-K')]
    reports = []

    for _, record in subset_idx.iterrows():
        date = record['Date Filed'] 
        raw_path = TEN_K_RAW + f"{ticker}_10-k_{date}.html"
        txt_path = TEN_K_PROCESSED + f"{ticker}_10-k_{date}.txt"
        print(f"Processing {raw_path}")

        url = r"https://www.sec.gov/Archives/" + record['File Name']
        report = DataSource(url, 
                            parse_10k, 
                            raw_path, 
                            txt_path)
        
        # assign so that report is downloaded
        txt = report.txt
        
        reports.append(report)
    
    return reports