import numpy as np
from metrics import (calculate_word_frequency, update_frequency, calculate_tfidf,
    calculate_textrank_similarty, calculate_lexrank_similarity, power_method)


def sumbasic_algorithm(sentences:list, word_matrix:list, limit_function, limit:int,)->list:
    """Calculates the SumBasic scores for all sentences and returns the highest-scoring ones."""

    word_frequencies = calculate_word_frequency(sentences, word_matrix)
    chosen_sentences = []
    count = 0

    # keep selecting sentences until the summary length is reached
    while count <= limit:
        sentence_scores = {}
        for sentence in range(len(sentences)):
            sentence_score = 0 
            sentence_length = len(word_matrix[sentence])

            # calculate the sentence score 
            for word in word_matrix[sentence]:
                sentence_score += word_frequencies[word]
            sentence_score /= sentence_length
            sentence_scores[sentence] = sentence_score

        # selecting the sentence with the highest score
        best_sentence = max(sentence_scores, key=sentence_scores.get)
        count += limit_function(sentences[best_sentence])
        chosen_sentences.append(sentences[best_sentence])
        del sentences[best_sentence]

         # decrease the word scores so the same words don't show up too many times
        word_frequencies = update_frequency(word_matrix[best_sentence], word_frequencies)

    # return the chosen sentences, expect for the last one because the limit was overstepped
    return chosen_sentences[:-1]


def tfidf_algorithm(sentences:list, word_matrix:list, limit_function, limit:int, category:str)->list:
    """Calculates the TFIDF scores for all sentences and returns the highest-scoring ones."""

    tfidf_scores = calculate_tfidf(sentences, word_matrix, category)

    chosen_sentences = []
    count = 0

    # keep selecting sentences until the summary length is reached
    while count <= limit:
        sentence_scores = {}
        for sentence in range(len(sentences)):
            sentence_score = 0 
            sentence_length = len(word_matrix[sentence])

            # calculate the sentence score
            for word in word_matrix[sentence]:
                sentence_score += tfidf_scores[word]
            sentence_score /= sentence_length
            sentence_scores[sentence] = sentence_score

        # select the best sentence
        best_sentence = max(sentence_scores, key=sentence_scores.get)
        count += limit_function(sentences[best_sentence])
        chosen_sentences.append(sentences[best_sentence])
        del sentences[best_sentence]

         # decrease the word scores, so the same words don't show up too many times
        tfidf_scores = update_frequency(word_matrix[best_sentence], tfidf_scores)

    # return the chosen sentences, expect for the last one because the limit was overstepped
    return chosen_sentences[:-1]


def textrank_algorithm(sentences:list, word_matrix:list, limit_function, limit:int, d:int,
    epsilon:int)->list:
    """Calculates the TextRank scores for all sentences and returns the highest-scoring ones."""

    similarities = calculate_textrank_similarty(sentences, word_matrix)
    degree = np.zeros(len(sentences))

    # divide by degree
    for similarity_row in range(len(similarities)):
        degree = sum(similarities[similarity_row])
        similarities[similarity_row] /= degree

    matrix = np.zeros((len(sentences), len(sentences)))

    # calculate the weights
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            total_score = (1-d) / len(word_matrix) + d * similarities[i][j]
            matrix[i][j] = total_score

    # calculate the sentence scores using the power method.
    vector = power_method(matrix, epsilon) 
    sentence_scores = dict(zip(sentences, vector))
    
    chosen_sentences = []
    count = 0

    while count <= limit:
        best_sentence = max(sentence_scores, key=sentence_scores.get)
        count += limit_function(best_sentence)
        chosen_sentences.append(best_sentence)
        del sentence_scores[best_sentence]

    # return the chosen sentences, expect for the last one because the limit was overstepped
    return chosen_sentences[:-1]



def lexrank_algorithm(sentences:str, word_matrix:str, limit_function, limit:int, category:str, 
    threshold=0.1, epsilon=0.1)->list:
    """Calculates the LexRank scores for all sentences and returns the highest-scoring ones."""

    matrix, degrees = calculate_lexrank_similarity(sentences, word_matrix, threshold, category)

    # divide each entry by the degree
    for i in range(len(sentences)):
        for j in range(len(sentences)):
            matrix[i][j] /= degrees[i]

    # apply the power method to obtain the sentence scores
    vector = power_method(matrix, epsilon)
    sentence_scores = dict(zip(sentences, vector))

    chosen_sentences = []
    count = 0

    # keep selecting sentences until the summary length is reached
    while count <= limit:
        best_sentence = max(sentence_scores, key=sentence_scores.get)
        count += limit_function(best_sentence)
        chosen_sentences.append(best_sentence)
        del sentence_scores[best_sentence]

    # return the chosen sentences, expect for the last one because the limit was overstepped
    return chosen_sentences[:-1]