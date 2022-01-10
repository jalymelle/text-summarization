from sys import exit
from data import get_text
from algorithms import (sumbasic_algorithm, tfidf_algorithm, textrank_algorithm, 
    lexrank_algorithm)    


def run(text_path:str, algorithm:str, stemmer='p', stopwords=True, limit_type='p', 
    limit_number=0.3, category='all', contains_title=False)->str:
    """Checks if all the inputs are valid are calls the algorithm."""
    
    # preprocessing: tokenizing into sentences and words, stemming, stop words
    sentences, words, title, original_length = get_text(text_path, contains_title, 
        stemmer, stopwords)
    
    # in case of stemming use stemmed idf file
    if stemmer == 'p' or stemmer == 'l':
        category = 'stemmed'

    # check which limit was selected
    limit_function, limit = check_limit(sentences, limit_type, limit_number, original_length)

    # for reordering the sentences at the end
    original_sentences = sentences.copy()

    # check which algorithm was selected and run it
    if algorithm == 'sumbasic':
        chosen_sentences = sumbasic_algorithm(sentences, words, limit_function, limit)

    elif algorithm == 'tfidf':
        chosen_sentences = tfidf_algorithm(sentences, words, limit_function, limit, category=category)

    elif algorithm == 'textrank':
        chosen_sentences = textrank_algorithm(sentences, words, limit_function, limit,  d=0.85, 
        epsilon=0.001)

    elif algorithm == 'lexrank':
        chosen_sentences = lexrank_algorithm(sentences, words, limit_function, limit, category=category, 
        threshold=0.1, epsilon=0.1)
    
    else:
        return exit('No possible algorithm selected.')
       
    # join the selected sentences together into a text
    summary = write_summary(chosen_sentences, original_sentences, title)

    return summary


def check_limit(sentences:list, limit_type:str, limit_number:int, original_length:int):
    """Returns the limit and the limit function."""

    if limit_type == 's' and limit_number > 0 and limit_number < len(sentences):
        limit_function = check_sentence_limit
        limit = limit_number

    elif limit_type == 'w' and limit_number > 0 and limit_number < original_length:
        limit_function = check_word_limit
        limit = limit_number

    elif limit_type == 'p' and limit_number > 0 and limit_number < 1:
        limit_function = check_word_limit
        limit = int(limit_number * original_length)
    
    else:
        exit('Impossible limit selected.')
    
    return limit_function, limit


def check_sentence_limit(sentence:list)->bool:
    """Returns the amount of sentences added. One in each step."""
    return 1


def check_word_limit(sentence:list)->bool:
    """Returns the amount of words added."""
    return len(sentence.split())


def write_summary(chosen_sentences:list, original_sentences:list, title:str):
    """Creates on string out of a list of sentences."""
    
    summary = ' '.join(sent.replace('\n', ' ') for sent in original_sentences if sent in chosen_sentences)

    # adding the title again
    if title:
        summary = title + '\n' + summary
    
    return summary
