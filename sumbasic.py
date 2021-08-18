from functions import get_sentences, calculate_word_frequency

# Einstellungen
summary_length = 2

all_sentences = get_sentences('doc.txt')

word_frequencies = calculate_word_frequency(all_sentences)



# Sätzen einen Score geben und den Satz mit dem höchsten Score auswählen bis gewünschte Länge erreicht wird.
# Score = durchschnittliche Wahrscheinlichkeit der Wörter im Satz.
chosen_sentences = []

while len(chosen_sentences) < summary_length:
    sentence_scores = {}

    for sentence in all_sentences:
        sentence_score = 0
        words = sentence.split(' ')
        sentence_length = len(words)
        for word in words:
            frequency = word_frequencies[word]
            sentence_score += frequency / sentence_length
        sentence_scores[sentence] = sentence_score


    # Satz mit höchstem Score auswählen
    best_sentence = max(sentence_scores)
    chosen_sentences.append(best_sentence)
    all_sentences.remove(best_sentence)

    # Worwahrscheinlichkeit der Wörter im Satz verringern, damit nicht zu oft das Gleiche in der Zusammenfassung vorkommt.
    for word in best_sentence.split(' '):
        word_frequencies[word] = word_frequencies[word] ** 2

summary = '. '.join(sentence for sentence in chosen_sentences)
print(summary)


