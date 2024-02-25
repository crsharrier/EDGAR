import os
from tqdm import tqdm
import pandas as pd
from nltk.tokenize import word_tokenize

from edgar.ref_data.tickers import get_sp100
from edgar.ref_data.sentiment_dict import get_sentiment_word_dict, transpose_dict
from edgar.constants import *

sp100_dict = get_sp100()
sentiment_dict = transpose_dict(get_sentiment_word_dict())
reports_10k = {}


def get_sentiment_counts_for_document(input_text: str) ->  dict:
    document_sentiments = {'Negative': 0, 'Positive': 0, 
                           'Uncertainty': 0, 'Litigious': 0, 
                           'Strong_Modal': 0, 'Weak_Modal': 0, 
                           'Constraining': 0, 'Total_Words': 0}

    #print('NOT TRANSPOSED')
    with tqdm(desc='Tokenizing...', leave=False) as pbar:
        words = input_text.split()
    with tqdm(total=len(words), desc='Counting...', leave=False) as pbar:
        for word in words:
            if word.upper() in sentiment_dict:
                s_list = sentiment_dict[word.upper()]
                for s in s_list:
                    document_sentiments[s] += 1
            pbar.update(1)
        document_sentiments['Total_Words'] = len(words)

    '''
    #print('TRANSPOSED')
    for word in words:
        for s, list in sentiment_dict.items():
            if word.upper() in list:
                document_sentiments[s] += 1
    '''
    
    
    return document_sentiments

'''
Take all the clean 10-k texts in the input folder.
Count words in the document belonging to a particular sentiment. 
Output the resulting dataframe to the output file.
'''
def write_document_sentiments(input_folder: str, 
                              output_file: str) -> None:
    input_names = os.listdir(input_folder)
    input_paths = [os.path.join(input_folder, name) for name in input_names]
    
    doc_sentiments = []

    with tqdm(total=len(input_paths), 
              desc='Getting sentiment word counts...') as pbar:  
        for file_name, path in zip(input_names, input_paths):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    clean_txt = f.read()
                
                doc_sentiment = get_sentiment_counts_for_document(clean_txt)
                doc_sentiment['Name'] = file_name.split('_')[0]
                doc_sentiment['Date'] = file_name.split('_')[2][:-4]
                doc_sentiments.append(doc_sentiment)
            except Exception as e:
                print(f"Error processing file {file_name}: {e}")
            finally:
                pbar.set_description(f'Getting sentiment word counts for: {file_name}')
                pbar.update(1)

    df = pd.DataFrame(doc_sentiments)
    try:
        df.to_csv(output_file)
    except PermissionError:
        print(f"Unable to save {output_file}. Is it being used by another program? (Excel?)")
