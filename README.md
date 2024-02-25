# EDGAR


- Can negative sentiment 10-k filings predict short term movements in share prices?
- Create a **package** to solve this

For each 10-k filing, count the number of words listed as 'Negative', 'Positive', 'Uncertain', etc..

Look for any correlations with short-term price movements.

#### Overview:

**ref_data**
- **get_sp100() -> pd.DataFrame**: return DataFrame with columns 'ticker' and 'entity_name'

- **get_ticker_cik() -> pd.DataFrame** return DataFrame with columns 'ticker' and 'cik'

- **get_yahoo_data() -> pd.DataFrame** - Return DataFrame containing historical price data for provided tickers.

- **get_sentiment_word_dict() -> dict** - Return a dictionary containing the LM sentiment words.

**downloader**

**cleaner**

**sentiment**

#### BACKLOG:
- **Unit tests** - I think most unit tests a broken now, as they are left over from an earlier version of the system.

- **Un-merge quarterly reports** - I think I might have merged quarterly 10-Ks into one txt per year. This leaves us with fewer 'date' data points to analyze against stock prices.

- **Reorganize data directory** - Simplify data directory structure. Write script to create this structure from a fresh first-run.