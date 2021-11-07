from data import get_sentences, get_words
from algorithms import (sumbasic_algorithm, tfidf_algorithm, textrank_algorithm, 
lexrank_algorithm)


def run(text_path:str, algorithm:str, length:int)->str:
    # preprocessing: tokenizing into sentences and words
    sentences = get_sentences(text_path)
    words = get_words(sentences, stem=True, remove_stopwords=True)

    if algorithm == 'sumbasic':
        chosen_sentences = sumbasic_algorithm(sentences, words, summary_length=length)

    elif algorithm == 'tfidf':
        chosen_sentences = tfidf_algorithm(sentences, words, summary_length=length)

    elif algorithm == 'textrank':
        chosen_sentences = textrank_algorithm(sentences, words, summary_length=length, 
        d=0.85, epsilon=0.001)

    elif algorithm == 'lexrank':
        chosen_sentences = lexrank_algorithm(sentences, words, summary_length=length, 
        threshold=0.1, epsilon=0.1)
    
    else:
        print('Please select an algorithm.')
    
    # joining the selected sentences together into a text.
    summary = ' '.join(sentence for sentence in sentences if sentence in chosen_sentences)
    
    return summary


path = r'data\BBC News Summary\News Articles\entertainment\005.txt'

summary_1 = run(path, 'lexrank', 4)

print(summary_1)