from metrics import (calculate_word_frequency, update_word_frequency, calculate_tfidf,
    calculate_textrank_similarty)
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


def textrank_algorithm(sentences:list, summary_length:int, d:int)->list:
    similarities = calculate_textrank_similarty(sentences)
    score_out = []
    for i in similarities: 
        score_out.append(sum(i))

    # nxn matrix of scores, set all scores to 1
    sentence_scores = [1 for sentence in sentences]

    # until convergence:
    for score in range(len(sentence_scores)):
        update = 0
        for i in range(len(sentences)):
            common_score = similarities[score][i]
            if common_score != 0:
                update += common_score * sentence_scores[i] / score_out[i] 

        updated_score = (1-d) + d * update
        sentence_scores[score-1] = updated_score


    # sort vertices based on final score
    final_scores = dict(zip(sentences, sentence_scores))

    chosen_sentences = []

    while len(chosen_sentences) < summary_length:
        best_sentence = max(final_scores, key=final_scores.get)
        chosen_sentences.append(best_sentence)
        del final_scores[best_sentence]
    
    return chosen_sentences
    


