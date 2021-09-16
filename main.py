from data import get_sentences
from algorithms import (sumbasic_algorithm, tfidf_algorithm, textrank_algorithm, 
lexrank_algorithm)


def run(text_path:str, algorithm:str, length:int)->str:
    all_sentences = get_sentences(text_path)

    if algorithm == 'sumbasic':
        chosen_sentences = sumbasic_algorithm(all_sentences, summary_length=length)

    elif algorithm == 'tfidf':
        chosen_sentences = tfidf_algorithm(all_sentences, summary_length=length)

    elif algorithm == 'textrank':
        chosen_sentences = textrank_algorithm(all_sentences, summary_length=length, 
        d=0.85, epsilon=0.001)

    elif algorithm == 'lexrank':
        chosen_sentences = lexrank_algorithm(all_sentences, summary_length=length, 
        threshold=0.1, epsilon=0.1)
    

    summary = ' '.join(sentence for sentence in chosen_sentences)
    return summary


#summary = run('sumbasic', 4)
#print(summary)
#summary = run('tfidf', 4)

#summary = run('textrank', 4)
path = r'data\BBC News Summary\News Articles\business\005.txt'

summary = run(path, 'lexrank', 4)

#print(summary)