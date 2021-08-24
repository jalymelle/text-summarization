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


def textrank_algorithm(sentences:list, summary_length:int, d:int, epsilon:int)->list:
    similarities = calculate_textrank_similarty(sentences)
    score_out = []
    for sentence in similarities: 
        score_out.append(sum(sentence))

    # nxn matrix of scores, set all scores to 0
    matrix = np.zeros((len(sentences), len(sentences)))

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if score_out[j] != 0:
                score = similarities[i][j] / score_out[j] 
            else:
                score = 0
        
        total_score = (1-d) + d * score
        matrix[i][j] = total_score
    
    # mit Hilfe
    p_vector = np.array([1.0 / len(sentences)] * len(sentences))
    lambda_ = 1.0

    while lambda_ > epsilon:
        next_p = np.dot(matrix.T, p_vector)
        lambda_ = np.linalg.norm(np.subtract(next_p, p_vector))
        p_vector = next_p 


    # sort vertices based on final score
    final_scores = dict(zip(sentences, p_vector))

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
        words_1 = word_tokenize(sentences[i])
        word_set = set(words_1)
        for j in range(len(sentences)):
            numerator = 0
            words_2 = word_tokenize(sentences[j])
            word_set.add(word for word in words_2)
            for word in words: 
                numerator += words_1.count(word) * words_2.count(word) 

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

    while len(chosen_sentences) < summary_length:
        best_sentence = max(final_scores, key=final_scores.get)
        chosen_sentences.append(best_sentence)
        del final_scores[best_sentence]
    
    return chosen_sentences


