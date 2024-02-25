import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)
import pandas as pd
from edgar.helpers import *

word_dict_csv_path = r"data\Loughran-McDonald_MasterDictionary_1993-2021.csv"

'''
Transpose sentiment dict from 
    {sentiments as keys (few keys): long lists of words}
    to 
    {words as keys (many keys): list of (usually one or two) sentiments} 
for faster lookup.

UPDATE test_get_sentiment_word_dict() proves that this was not, 
in fact, faster. This will not be used.
'''
def transpose_dict(orig_dict: dict) -> dict:
    new_dict = {}
    for sentiment, words in orig_dict.items():
        for word in words:
            if word in new_dict:
                new_dict[word].append(sentiment)
            else:
                new_dict[word] = [sentiment]       
    return new_dict

'''
Return a dictionary containing the LM sentiment words.
The keys for the dictionary are the sentiments, 
and the values will be a list of words associated with that particular sentiment.
'''
def get_sentiment_word_dict() -> dict:
    df = pd.read_csv(word_dict_csv_path)

    columns = ['Negative', 'Positive', 'Uncertainty', 'Litigious', 
               'Strong_Modal', 'Weak_Modal', 'Constraining']
    sentiment_dict = {category: [] for category in columns}
    for category in columns:
        index_list = df[df[category] != 0].index
        for idx in index_list:
            word = df.iloc[idx, df.columns.get_loc('Word')]
            sentiment_dict[category].append(word)

    return sentiment_dict
