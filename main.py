import json
from colorama import Fore
from edgar.ref_data import get_sp100, get_ticker_cik, get_sentiment_word_dict, get_yahoo_data
from edgar.downloader import write_page, download_files_10k
from edgar.cleaner import  clean_html_text, write_clean_html_json_files
from edgar.sentiment import get_sentiment_dict_for_document, write_document_sentiments

test_artefacts_dir = 'tests/artefacts/'

# ===============================================================================
# ref_data
# ===============================================================================
def ref_data():

    # get_sp100():
    # ===================================================
    entity_dict = get_sp100()

    print(Fore.CYAN + "get_sp100():" + Fore.RESET)
    print(Fore.GREEN + f"\t{len(entity_dict)} entities in entity_dict")
    print(f"\tsample rows:")
    for i in range (0, 3):
        print(f"\t\t{list(entity_dict.items())[i]}")
    print(Fore.RESET, end='')

    # get_ticker_cik():
    # ===================================================
    ticker_cik = get_ticker_cik()

    print(Fore.CYAN + "get_ticker_cik():" + Fore.RESET)
    print(Fore.GREEN + f"\t{len(ticker_cik)} tickers in ticker_cik_df")
    print(f"\tsample rows:")
    for i in range (0, 3):
        print(f"\t\t{list(ticker_cik.items())[i]}")
    print(Fore.RESET, end='')


    # get_sentiment_word_dict():
    # ===================================================
    # sentiment_dict = get_sentiment_word_dict()
    # sentiment_dict_file = test_artefacts_dir + "sentiment_dict.json"
    # with open(test_artefacts_dir + 'sentiment_dict.json', 'w') as f:
    #      json.dump(sentiment_dict, f)

    # print(Fore.CYAN + "get_sentiment_word_dict():" + Fore.RESET)
    # print(Fore.GREEN + f"\tsentiment_dict written to: {sentiment_dict_file}" + Fore.RESET)

    # # get_yahoo_data():
    # # ===================================================
    # start_date = '2000-01-01'
    # end_date = '2020-01-01'
    # tickers = ['AAPL']
    # df = get_yahoo_data(start_date, end_date, tickers)
    # csv_path = test_artefacts_dir + f"{'_'.join(tickers)}.csv"
    # df.to_csv(csv_path)

    # print(Fore.CYAN + "get_yahoo_data():" + Fore.RESET)
    # print(Fore.GREEN + f"\tyahoo data written to: {csv_path}" + Fore.RESET)

# ===============================================================================
# downloader
# ===============================================================================
def downloader():
    test_10k_url = r"https://www.sec.gov/Archives/edgar/data/1018724/000101872424000008/amzn-20231231.htm"
    test_page_path = test_artefacts_dir + r"AMZN_10k_date.html"

    ticker = 'TSLA' 
    dest_folder = "edgar/requests_cache/10k_raw/"

    # get_cik_df():
    # ===================================================
    # cik_df = get_cik_df()

    # print(Fore.CYAN + "get_cik_df():" + Fore.RESET)
    # print(Fore.GREEN + f"\tcik_df contains {len(cik_df)} entities:")
    # print(cik_df.head())
    # print(Fore.RESET, end='')

    # write_page():
    # # ===================================================
    # print(Fore.CYAN + "write_page():" + Fore.RESET)
    # if write_page(test_10k_url, test_page_path):
    #    print(Fore.GREEN + f"\twrite_page(): HTML content successfully written to {test_page_path}" + Fore.RESET)
    

    # download_files_10k():
    # ===================================================
    download_files_10k(ticker, dest_folder)


# ===============================================================================
# cleaner
# ===============================================================================
def cleaner():
    test_html_file = r"tests\artefacts\AMZN_10k_date.html"
    
    input_dir = r"edgar\requests_cache\10k_raw"
    output_dir = r"edgar\requests_cache\10k_clean"

    # clean_html_text():
    # ===================================================
    # with open(test_html_file, 'r') as f:
    #     test_html_str = f.read()
    # cleaned_str = clean_html_text(test_html_str)
    # #print(cleaned_str[:5000])
    # with open(test_html_file + r"_clean.html", 'w', encoding='utf-8') as f:
    #     f.write(cleaned_str)

    # write_clean_html_text_files():
    # ===================================================
    write_clean_html_json_files(input_dir, output_dir)


# ===============================================================================
# sentiment
# ===============================================================================
def sentiment():
    # clean_txt_path = r"tests\artefacts\cleaned_html\a10-k20199282019.htm"
    # with open(clean_txt_path, 'r', encoding='utf-8') as f:
    #     clean_txt = f.read()
    # sentiment_dict = get_sentiment_dict_for_document(clean_txt)
    #print(sentiment_dict)

    clean_html_folder = r"tests\artefacts\cleaned_html"
    sentiments_df_file = r"edgar\requests_cache\10k_sentiments\sentiments.csv"
    write_document_sentiments(clean_html_folder, sentiments_df_file)

# ===============================================================================
# main
# ===============================================================================
if __name__ == '__main__':

    #ref_data()
    downloader()
    cleaner()
    sentiment()