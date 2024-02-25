from edgar.wordcount import write_document_sentiments
from edgar.ten_k import download_files_10k
from edgar.ref_data.tickers import get_sp100
from edgar.ref_data.yahoo import get_yahoo_data
from edgar.constants import *
from edgar.helpers import Timer

sp100 = get_sp100()
tickers = [t for t in sp100] 
num_errors = 0

with Timer('download_reports_fresh'):
    for t in tickers:
        try:
            download_files_10k(t, 2013)
        except KeyboardInterrupt:
            break
        except :
            num_errors += 1
            continue

with Timer('write_document_sentiments()'):
    write_document_sentiments(TEN_K_PROCESSED, SENTIMENTS_PATH)

with Timer('get_yahoo_data()'):
    yahoo_df = get_yahoo_data('2013-01-01', '2013-12-31', tickers)
    yahoo_df.to_csv(YAHOO_PATH)

# print(f"num_errors = {num_errors}") 
