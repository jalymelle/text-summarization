from data import get_sentences
from algorithms import sumbasic_algorithm, tfidf_algorithm, textrank_algorithm, lexrank_algorithm


def run(algorithm:str)->str:
    all_sentences = get_sentences(r'data\BBC News Summary\News Articles\business\002.txt')

    if algorithm == 'sumbasic':
        chosen_sentences = sumbasic_algorithm(all_sentences, summary_length=2)

    elif algorithm == 'tfidf':
        chosen_sentences = tfidf_algorithm(all_sentences, summary_length=2)

    elif algorithm == 'textrank':
        chosen_sentences = textrank_algorithm(all_sentences, summary_length=2, d=0.85, epsilon=0.001)

    elif algorithm == 'lexrank':
        chosen_sentences = lexrank_algorithm(all_sentences, summary_length=2, threshold=0.1, epsilon=0.1)
    

    summary = ' '.join(sentence for sentence in chosen_sentences)
    return summary


summary = run('sumbasic')
print('Sumbasic', summary)

summary = run('tfidf')
print('TFIDF', summary)

summary = run('textrank')
print('TextRank', summary)

summary = run('lexrank')
print('LexRank', summary)