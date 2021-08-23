from data import get_sentences
from algorithms import sumbasic_algorithm, tfidf_algorithm, textrank_algorithm, lexrank_algorithm

all_sentences = get_sentences('doc.txt')
algorithm = 'lexrank'

if algorithm == 'sumbasic':
    chosen_sentences = sumbasic_algorithm(all_sentences, summary_length=2)

elif algorithm == 'tfidf':
    chosen_sentences = tfidf_algorithm(all_sentences, summary_length=2)

elif algorithm == 'textrank':
    chosen_sentences = textrank_algorithm(all_sentences, summary_length=2, d=0.85)

elif algorithm == 'lexrank':
    chosen_sentences = lexrank_algorithm(all_sentences, summary_length=2, threshold=0.1, epsilon=0.1)

summary = ' '.join(sentence for sentence in chosen_sentences)
print(summary)