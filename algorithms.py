from metrics import calculate_word_frequency, update_word_frequency, calculate_tfidf
from nltk.tokenize import word_tokenize


# Sätzen einen Score geben und den Satz mit dem höchsten Score auswählen bis gewünschte Länge erreicht wird.
# Score = durchschnittliche Wahrscheinlichkeit der Wörter im Satz.
def sumbasic_algorithm(sentences: list, summary_length: int)->list:
    chosen_sentences = []
    word_frequencies = calculate_word_frequency(sentences)
    while len(chosen_sentences) < summary_length:
        sentence_scores = {}
        for sentence in sentences:
                sentence_score = 0
                words = word_tokenize(sentence)
                sentence_length = len(words)
                for word in words:
                    frequency = word_frequencies[word]
                    sentence_score += frequency / sentence_length
                sentence_scores[sentence] = sentence_score

        # Satz mit höchstem Score auswählen
        best_sentence = max(sentence_scores)
        chosen_sentences.append(best_sentence)
        sentences.remove(best_sentence)

        word_frequencies = update_word_frequency(best_sentence, word_frequencies)
    return chosen_sentences


def tfidf_algorithm(sentences:list, summary_length:int)->list:
    tfidf_scores = calculate_tfidf(sentences)
    chosen_sentences = []

    while len(chosen_sentences) < summary_length:
        sentence_scores = {}

        for sentence in sentences:
            sentence_score = 0
            words = word_tokenize(sentence)
            sentence_length = len(words)
            for word in words:
                frequency = tfidf_scores[word]
                sentence_score += frequency / sentence_length
            sentence_scores[sentence] = sentence_score


        # Satz mit höchstem Score auswählen
        best_sentence = max(sentence_scores)
        chosen_sentences.append(best_sentence)
        sentences.remove(best_sentence)
    
        tfidf_scores = update_word_frequency(best_sentence, tfidf_scores)
    return chosen_sentences
    


