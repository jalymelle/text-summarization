from functions import (calculate_inverse_document_frequency, 
    calculate_word_frequency, get_sentences)

# Text in Sätze aufteilen
all_sentences = get_sentences('doc.txt')

summary_length = 2

threshold = 0.1
# create list of all words
tfidf_words = {}

# TF berechnen
word_frequencies = calculate_word_frequency(all_sentences)

# IDF berechnen
inverse_document_frequencies = calculate_inverse_document_frequency(all_sentences)

# get tfidf scores for each word
for sentence in all_sentences:
    for word in sentence.split(' '):
        # compute tfidf
        tfidf = word_frequencies[word] * inverse_document_frequencies[word]
        tfidf_words[word] = tfidf

sentence_scores = []
for i in range(len(all_sentences)):
    score = 0
    for word in all_sentences[i].split(' '):
        score += tfidf_words[word]
    sentence_scores.append(score)

chosen_sentences = []

while len(chosen_sentences) < summary_length:
    sentence_scores = {}

    for sentence in all_sentences:
        sentence_score = 0
        words = sentence.split(' ')
        sentence_length = len(words)
        for word in words:
            frequency = tfidf_words[word]
            sentence_score += frequency / sentence_length
        sentence_scores[sentence] = sentence_score


    # Satz mit höchstem Score auswählen
    best_sentence = max(sentence_scores)
    chosen_sentences.append(best_sentence)
    all_sentences.remove(best_sentence)

    # Worwahrscheinlichkeit der Wörter im Satz verringern, damit nicht zu oft das Gleiche in der Zusammenfassung vorkommt.
    for word in best_sentence.split(' '):
        tfidf_words[word] = tfidf_words[word] ** 2

summary = '. '.join(sentence for sentence in chosen_sentences)
print(summary)