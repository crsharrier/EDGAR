# EDGAR


- Can negative sentiment 10-k filings predict short term movements in share prices?
- Create a **package** to solve this

For each 10-k filing, count the number of words listed as 'Negative', 'Positive', 'Uncertain', etc..

Look for any correlations with short-term price movements.

#### Overview:

**ref_data**
- **get_sp100() -> pd.DataFrame**: return DataFrame with columns 'ticker' and 'entity_name'

- **get_ticker_cik() -> pd.DataFrame** return DataFrame with columns 'ticker' and 'cik'



**downloader**

**cleaner**

**sentiment**