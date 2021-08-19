from data import get_sentences
from metrics import calculate_word_frequency
from algorithms import sumbasic_algorithm

all_sentences = get_sentences('doc.txt')
word_frequencies = calculate_word_frequency(all_sentences)


chosen_sentences = sumbasic_algorithm(all_sentences, word_frequencies, summary_length=2)
summary = ' '.join(sentence for sentence in chosen_sentences)
print(summary)