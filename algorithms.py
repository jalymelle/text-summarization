from metrics import update_word_frequency


# Sätzen einen Score geben und den Satz mit dem höchsten Score auswählen bis gewünschte Länge erreicht wird.
# Score = durchschnittliche Wahrscheinlichkeit der Wörter im Satz.
def sumbasic_algorithm(sentences: list, word_frequencies, summary_length: int)->list:
    chosen_sentences = []
    while len(chosen_sentences) < summary_length:
        sentence_scores = {}
        for sentence in sentences:
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
        sentences.remove(best_sentence)

        word_frequencies = update_word_frequency(word_frequencies, best_sentence)
    return chosen_sentences


