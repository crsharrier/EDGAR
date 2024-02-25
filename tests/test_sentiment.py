import pytest
from edgar.helpers import *
from edgar.ref_data.sentiment_dict import get_sentiment_word_dict, \
    transpose_dict
from edgar.wordcount import get_sentiment_counts_for_document

# TODO: GET BETTER TEXT
@pytest.fixture
def clean_text():
    file_path = r"edgar\requests_cache\10k_clean\TSLA_10-k_date.html"
    with open(file_path, 'r', encoding='utf-8') as f:
        return f.read()

@pytest.fixture
def sentiment_dict():
    return get_sentiment_word_dict()

@pytest.fixture
def transposed_sentiment_dict(sentiment_dict):
    return transpose_dict(sentiment_dict)

def test_get_sentiment_word_dict(sentiment_dict):
    total_words = 0
    with Colour(DEBUG_HEADER):
        print("get_sentiment_word_dict()")

    for category in sentiment_dict.keys():
        num_words = len(sentiment_dict[category])
        with Colour(DEBUG):
            print(f"\t{category} has {num_words} words")
        total_words += num_words

    with Colour(DEBUG_HEADER):
        print(f"\tTotal = {total_words} words")

    assert len(sentiment_dict) == 7
    
def test_transposed_sentiment_dict(transposed_sentiment_dict):
    num_keys = len(transposed_sentiment_dict)
    more_than_one_sentiment = \
        {k: v for k, v in transposed_sentiment_dict.items() if len(v) > 1}
    
    with Colour(DEBUG_HEADER):
        print(f"transpose_dict():")
    with Colour(DEBUG):
        print(f"\ttransposed dict has {num_keys} words.")
        print(f"\t{len(more_than_one_sentiment)} of these have more than one sentiment.")

    sentiments = []
    for sentiment_list in transposed_sentiment_dict.values():
        for s in sentiment_list:
            if s not in sentiments:
                sentiments.append(s)
    assert len(sentiments) == 7

def test_compare_dict_lookup_speed(sentiment_dict, 
                                   transposed_sentiment_dict, 
                                   clean_text):
    errors = []
    with Timer('orig_dict') as timer:
        orig_counts = get_sentiment_counts_for_document(
            sentiment_dict, clean_text, transposed=False
            )
    orig_time = timer.duration

    with Timer('transposed_dict') as timer:
        trans_counts = get_sentiment_counts_for_document(
            transposed_sentiment_dict, clean_text, transposed=True
            )
    trans_time = timer.duration

    diff = orig_time - trans_time
    s_f = 'quicker' if diff > 0 else 'slower'
    slowest = max(trans_time, orig_time)
    fastest = min(trans_time, orig_time)
    times = slowest / fastest
    with Colour(DEBUG):
        print(f"Transposed lookup (many keys) completed...\n\t \
              {diff: .4f} seconds / {times: .4f} times {s_f}\n\t\t\
                ...than non-transposed lookup")
        
    if orig_counts != trans_counts:
        errors.append('TEST INVALID - the two conditions did not produce the same resulting dictionary.')
    if diff < 0:
        with Colour(ERROR):
            print('Transposed was not quicker than original.')
    else:
        with Colour():
            print('Transposed was quicker than original.')

    print(orig_counts)
    print(trans_counts)
    assert not errors, "errors occured:\n{}".format("\n".join(errors))
    
