from math import log10, sqrt
import numpy as np
from data import get_words, collect_all_words
from nltk.tokenize import sent_tokenize

def calculate_word_frequency(sentences:list)->dict:
    word_frequencies = {}
    num_words = 0

    # Count how often each word occurs in the text.
    for sentence in sentences:
        words = get_words(sentence, True)
        for word in words:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else: 
                word_frequencies[word] += 1
            num_words += 1

    # Divide the number of times each word occurs by the number of words in the text.
    for frequency in word_frequencies:
        word_frequencies[frequency] = word_frequencies[frequency] / num_words
    return word_frequencies


def calculate_inverse_document_frequency(sentences:list)->dict:
    all_words = collect_all_words()
    # Extra lines to check for errors
    #all_words = []
    #for sentence in sentences:
        #all_words.append(set(sentences))
    inverse_document_frequencies = {}

    for sentence in sentences:
        words = get_words(sentence, True)
        for word in words:
            # Find the number of documents that contain the word.
            if word not in inverse_document_frequencies:
                num_contain_word = 1
            for word_set in all_words:
                if word in word_set:
                    num_contain_word += 1
            # Divide the total number of documents by the number of documents 
            # that contain the word.
            inverse_document_frequencies[word] = log10(len(all_words) / num_contain_word)
    return inverse_document_frequencies


def update_frequency(sentence:str, frequency_dict:dict)->dict:
    """Decreases the word probability of the words in the chosen sentence."""
    words = get_words(sentence, True)
    for word in words:
        frequency_dict[word] = frequency_dict[word] ** 2
    return frequency_dict


def calculate_tfidf(sentences:list)->dict:
    word_frequencies = calculate_word_frequency(sentences)
    inverse_document_frequencies = calculate_inverse_document_frequency(sentences)
    tfidf_scores = {}

    for sentence in sentences:
        words = get_words(sentence, True)
        for word in words:
            # Calculate the tfidf score by multiplying the word frequency and 
            # the inverse document frequency.
            tfidf = word_frequencies[word] * inverse_document_frequencies[word]
            tfidf_scores[word] = tfidf
    return tfidf_scores


def calculate_textrank_similarty(sentences:list)->list:
    similarities = []
    score_out = []

    for sentence_1 in sentences:
        sentence_similarities = []
        for sentence_2 in sentences:
            # Find the number of words that are in both sentences.
            words_in_common = 0
            words_1 = get_words(sentence_1, True)
            words_2 = get_words(sentence_2, True)
            for word in words_1:
                if word in words_2:
                    words_in_common += 1
            
            # Divide the words in both sentences by the sentence lengths.
            similarity = words_in_common / (log10(len(sentence_1)) * log10(len(sentence_2)))
            sentence_similarities.append(similarity)

        similarities.append(sentence_similarities)

    for sentence in similarities: 
        # Calculate the sum of all sentence weights.
        score_out.append(sum(sentence))

    return similarities, score_out


def power_method(sentences:list, matrix:list, epsilon:int)->list:
    p_vector = np.array([1.0 / len(sentences)] * len(sentences))
    lambda_ = 1.0

    while lambda_ > epsilon:
        next_p = np.dot(matrix.T, p_vector)
        lambda_ = np.linalg.norm(np.subtract(next_p, p_vector))
        p_vector = next_p
    
    return p_vector


def calculate_lexrank_similarity(sentences:list, threshold:int)->list:
    idf = calculate_inverse_document_frequency(sentences)
    sentence_denominators = []

    for sentence in sentences:
        # Multiply the word frequencies and inverse document frequencies of each word 
        # in the sentence to calculate the sentence denominator. 
        sentence_tfidf = 0 
        words = get_words(sentence, True)
        word_set = set(words)
        for word in word_set:
            tf = words.count(word)
            sentence_tfidf += tf * idf[word] ** 2
        sentence_denominators.append(sentence_tfidf)
    
    
    matrix = np.zeros((len(sentences), len(sentences)))
    degrees = []

    for i in range(len(sentences)):
        sentence_degree = 1
        words_1 = get_words(sentences[i], True)
        for j in range(len(sentences)):
            numerator = 0
            words_2 = get_words(sentences[j], True)
            # Word_set is the set of all words in sentences i and j.
            word_set = set.union(set(words_1), set(words_2))

            for word in word_set: 
                # Numerator for two sentences: Multiply the word frequencies 
                # of each word in the sentences and its inverse document frequency.
                numerator += words_1.count(word) * words_2.count(word) * idf[word] ** 2
            
            # Denominator for two sentences: Square root of the previously calculated
            # sentence denominators.
            denominator = (sqrt(sentence_denominators[i]) * sqrt(sentence_denominators[j]))
            idf_cosine = numerator / denominator

            if idf_cosine > threshold:
                # If the sentences are similar enough (idf_cosine > threshold), set the
                # weight of the two sentences to 1.
                matrix[i][j] = 1
                sentence_degree += 1
            else:
                matrix[i][j] = 0
        degrees.append(sentence_degree)
    
    return matrix, degrees