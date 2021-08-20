from data import get_sentences
from algorithms import sumbasic_algorithm, tfidf_algorithm

all_sentences = get_sentences('doc.txt')
algorithm = 'tfidf'

if algorithm == 'sumbasic':
    chosen_sentences = sumbasic_algorithm(all_sentences, summary_length=2)

elif algorithm == 'tfidf':
    chosen_sentences = tfidf_algorithm(all_sentences, summary_length=2)

summary = ' '.join(sentence for sentence in chosen_sentences)
print(summary)