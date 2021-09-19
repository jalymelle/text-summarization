import numpy as np
from data import get_words
from metrics import (calculate_word_frequency, update_frequency, calculate_tfidf,
    calculate_textrank_similarty, calculate_lexrank_similarity, power_method)


def sumbasic_algorithm(sentences: list, summary_length: int)->list:
    word_frequencies = calculate_word_frequency(sentences)
    sentence_scores = {}

    # Keep selecting sentences until the summary length is reached.
    chosen_sentences = []

    while len(chosen_sentences) < summary_length:
        for sentence in sentences:
            sentence_score = 0
            words = get_words(sentence, True)
            sentence_length = len(words)

            # Calculate the sentence score by summing up all word frequencies 
            # of the words in the sentence.
            for word in words:
                sentence_score += word_frequencies[word]
            sentence_score /= sentence_length
            sentence_scores[sentence] = sentence_score

        best_sentence = max(sentence_scores, key=sentence_scores.get)
        chosen_sentences.append(best_sentence)
        del sentence_scores[best_sentence]

         # Decrease the word scores, so the same words don't show up too many times.
        word_frequencies = update_frequency(best_sentence, word_frequencies)

    return chosen_sentences


def tfidf_algorithm(sentences:list, summary_length:int)->list:
    tfidf_scores = calculate_tfidf(sentences)
    sentence_scores = {}

    # Keep selecting sentences until the summary length is reached.
    chosen_sentences = []

    while len(chosen_sentences) < summary_length:
        for sentence in sentences:
            sentence_score = 0
            words = get_words(sentence, True)
            sentence_length = len(words)

            # Calculate the sentence score by summing up all word frequencies 
            # of the words in the sentence.
            for word in words:
                sentence_score += tfidf_scores[word]
            sentence_score /= sentence_length
            sentence_scores[sentence] = sentence_score

        best_sentence = max(sentence_scores, key=sentence_scores.get)
        chosen_sentences.append(best_sentence)
        del sentence_scores[best_sentence]

         # Decrease the word scores, so the same words don't show up too many times.
        tfidf_scores = update_frequency(best_sentence, tfidf_scores)

    return chosen_sentences


def textrank_algorithm(sentences:list, summary_length:int, d:int, epsilon:int)->list:
    similarities, score_out = calculate_textrank_similarty(sentences)
    matrix = np.zeros((len(sentences), len(sentences)))

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            if score_out[j] != 0:
                score = similarities[i][j] / score_out[j] 
            else:
                score = 0
        
        # Calculate the TextRank score.
        total_score = (1-d) + d * score
        matrix[i][j] = total_score
    
    vector = power_method(sentences, matrix, epsilon) 
    sentence_scores = dict(zip(sentences, vector))

    # Keep selecting sentences until the summary length is reached.
    chosen_sentences = []

    while len(chosen_sentences) < summary_length:
        best_sentence = max(sentence_scores, key=sentence_scores.get)
        chosen_sentences.append(best_sentence)
        del sentence_scores[best_sentence]
    
    return chosen_sentences


def lexrank_algorithm(sentences:list, summary_length:int, threshold:int, epsilon:int)->list:
    matrix, degrees = calculate_lexrank_similarity(sentences, threshold)

    for i in range(len(sentences)):
        for j in range(len(sentences)):
            matrix[i][j] /= degrees[i]

    vector = power_method(sentences, matrix, epsilon)
    sentence_scores = dict(zip(sentences, vector))

    # Keep selecting sentences until the summary length is reached.
    chosen_sentences = []

    while len(chosen_sentences) < summary_length:
        best_sentence = max(sentence_scores, key=sentence_scores.get)
        chosen_sentences.append(best_sentence)
        del sentence_scores[best_sentence]
    
    return chosen_sentences


