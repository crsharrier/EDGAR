from edgar.ref_data import get_sentiment_word_dict
from nltk.tokenize import word_tokenize
import pandas as pd
import os

def transpose_dict(orig_dict: dict) -> dict:
    new_dict = {}
    for sentiment, words in orig_dict.items():
        for word in words:
            new_dict[word] = sentiment
    return new_dict

sentiments = transpose_dict(get_sentiment_word_dict())

def get_sentiment_dict_for_document(input_text: str) ->  dict:
    document_sentiments = {'Negative': 0, 'Positive': 0, 
                           'Uncertainty': 0, 'Litigious': 0, 
                           'Strong_Modal': 0, 'Weak_Modal': 0, 
                           'Constraining': 0}
    words = word_tokenize(input_text)
    for word in words:
        if word.upper() in sentiments:
            sentiment = sentiments[word.upper()]
            document_sentiments[sentiment] += 1
    
    return document_sentiments
        

# Take all the clean 10-k texts in the input folder.
# Count words in the document belonging to a particular sentiment. 
# Output the resulting dataframe to the output file.
def write_document_sentiments(input_folder: str, 
                              output_file: str) -> None:
    input_names = os.listdir(input_folder)
    input_paths = [os.path.join(input_folder, name) for name in input_names]

    doc_sentiments = []
    for name, path in zip(input_names, input_paths):
        with open(path, 'r', encoding='utf-8') as f:
            clean_txt = f.read()
        doc_sentiment = get_sentiment_dict_for_document(clean_txt)
        doc_sentiment['name'] = name
        doc_sentiments.append(doc_sentiment)

    df = pd.DataFrame(doc_sentiments)
    try:
        df.to_csv(output_file)
    except PermissionError:
        print(f"Unable to save {output_file}. Is it being used by another program? (Excel?)")
