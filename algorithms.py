from metrics import (calculate_word_frequency, update_word_frequency, calculate_tfidf,
    calculate_textrank_similarty, calculate_inverse_document_frequency)
from nltk.tokenize import word_tokenize
from math import sqrt
import numpy as np

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
    for sentence in similarities: 
        score_out.append(sum(sentence))

    # nxn matrix of scores, set all scores to 1
    sentence_scores = [1 for sentence in sentences]

    # until convergence:
    for i in range(len(sentence_scores)):
        update = 0
        for j in range(len(sentences)):
            common_score = similarities[i][j]
            if common_score != 0:
                update += common_score * sentence_scores[j] / score_out[j] 

        updated_score = (1-d) + d * update
        sentence_scores[i-1] = updated_score


    # sort vertices based on final score
    final_scores = dict(zip(sentences, sentence_scores))

    chosen_sentences = []

    while len(chosen_sentences) < summary_length:
        best_sentence = max(final_scores, key=final_scores.get)
        chosen_sentences.append(best_sentence)
        del final_scores[best_sentence]
    
    return chosen_sentences

def lexrank_algorithm(sentences:list, summary_length:int, threshold:int, epsilon:int)->list:
    # create matrix of cosine similarities
    idf = calculate_inverse_document_frequency(sentences)
    sentence_denominators = []

    for sentence in sentences:
        sentence_tfidf = 0 
        words = word_tokenize(sentence)
        word_set = set(words)
        for word in word_set:
            tf = words.count(word)
            sentence_tfidf += tf * idf[word] ** 2
        sentence_denominators.append(sentence_tfidf)
    
    matrix = np.zeros((len(sentences), len(sentences)))
    degrees = []

    for i in range(len(sentences)):
        sentence_degree = 1
        sentence_1 = sentences[i].split(' ')
        words = set(word for word in sentence_1)
        for j in range(len(sentences)):
            numerator = 0
            sentence_2 = sentences[j].split(' ')
            words.add(word for word in sentence_2)
            for word in words: 
                numerator += sentence_1.count(word) * sentence_2.count(word) 

            idf_cosine = numerator / (sqrt(sentence_denominators[i]) * sqrt(sentence_denominators[j]))
            if idf_cosine > threshold:
                matrix[i][j] = 1
                sentence_degree += 1
            else:
                matrix[i][j]
        degrees.append(sentence_degree)

        
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            matrix[i][j] /= degrees[i]


    # mit Hilfe
    p_vector = np.array([1.0 / len(sentences)] * len(sentences))
    lambda_ = 1.0

    while lambda_ > epsilon:
        next_p = np.dot(matrix.T, p_vector)
        lambda_ = np.linalg.norm(np.subtract(next_p, p_vector))
        p_vector = next_p 


    final_scores = dict(zip(sentences, p_vector))
    chosen_sentences = []
    summary_length = 2

    while len(chosen_sentences) < summary_length:
        best_sentence = max(final_scores, key=final_scores.get)
        chosen_sentences.append(best_sentence)
        del final_scores[best_sentence]
    
    return chosen_sentences


