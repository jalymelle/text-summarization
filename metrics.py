import ast
import numpy as np
from math import log, sqrt

def calculate_word_frequency(sentences:list, word_matrix:list)->dict:
    """Returns a dictionary of each word and its frequency."""
    
    word_frequencies = {}
    num_words = 0

    # count how often each word occurs in the text
    for sentence in range(len(sentences)):
        for word in word_matrix[sentence]:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else: 
                word_frequencies[word] += 1
            num_words += 1

    # divide frequency count by total number of words
    for frequency in word_frequencies:
        word_frequencies[frequency] = word_frequencies[frequency] / num_words

    return word_frequencies


def calculate_inverse_document_frequency(sentences:list, word_matrix:list, category:str)->dict:
    """Returns a dictionary of each word with its inverse document frequency."""

    num_documents = {'business': 510, 'entertainment': 386, 'politics': 417,
        'sport': 511, 'tech': 401, 'all': 2225, 'stemmed': 2225}

    inverse_document_frequencies = {}

    # check how rare the words are by comparing with other documents
    with open(r'data\BBC News Summary\idf\\' + category + "_idf.txt", 'r') as document:
        document = document.read()
        all_idf_frequencies = ast.literal_eval(document)

    for sentence in range(len(sentences)):
        for word in word_matrix[sentence]:
            # check if the word has an inverse document frequency
            if word not in all_idf_frequencies:
                num_contain_word = 1

            # find the number of documents that contain the word
            else: 
                num_contain_word = all_idf_frequencies[word] + 1

            inverse_document_frequencies[word] = log(num_documents[category] / num_contain_word)
    return inverse_document_frequencies


def update_frequency(words:list, frequency_dict:dict)->dict:
    """Decreases the word probability of the words in the chosen sentence."""  

    for word in words:
        frequency_dict[word] = frequency_dict[word] ** 2

    return frequency_dict


def calculate_tfidf(sentences:list, word_matrix:list, category:str)->dict:
    """Returns a dictionary of each word with its tfidf score."""

    tfidf_scores = {}
    word_frequencies = calculate_word_frequency(sentences, word_matrix)
    inverse_document_frequencies = calculate_inverse_document_frequency(sentences, word_matrix, category)

    for sentence in range(len(sentences)):
        for word in word_matrix[sentence]:
            # calculate the tfidf score 
            tfidf = word_frequencies[word] * inverse_document_frequencies[word]
            tfidf_scores[word] = tfidf

    return tfidf_scores


def calculate_textrank_similarty(sentences:list, word_matrix:list)->list:
    """Returns a matrix of the similarities between two sentences 
    and the sum of all sentence weights for each sentence."""

    similarities = np.zeros((len(sentences), len(sentences)))

    for sentence_1 in range(len(sentences)):
        for sentence_2 in range(len(sentences)):
            # find the number of words that are in both sentences
            words_in_common = 0
            words_1 = word_matrix[sentence_1]
            words_2 = word_matrix[sentence_2]
            for word in words_1:
                if word in words_2:
                    words_in_common += 1
            
            # divide the words in both sentences by the sentence lengths
            similarity = words_in_common / (log(len(words_1)) + log(len(words_2)))
            similarities[sentence_1][sentence_2] = similarity
    return similarities



def calculate_lexrank_similarity(sentences:list, word_matrix:list, threshold:int, category:str)->list:
    """Returns a matrix of sentences with 1 if the sentences are similar and 0 if they
    are not and the total number of similarities for each sentence."""

    # calculate the tfidf score of each sentence 
    idf = calculate_inverse_document_frequency(sentences, word_matrix, category)
    sentence_denominators = []

    for sentence in range(len(sentences)):
        sentence_tfidf = 0 
        words = word_matrix[sentence]
        for word in set(words):
            tf = words.count(word)
            sentence_tfidf += (tf * idf[word]) ** 2
        sentence_denominators.append(sentence_tfidf)
    
    # create a matrix of similarities
    similarities = np.zeros((len(sentences), len(sentences)))
    degrees = np.zeros(len(sentences))

    for sent_1 in range(len(sentences)):
        sentence_degree = 0
        words_1 = word_matrix[sent_1]
        for sent_2 in range(len(sentences)):
            numerator = 0
            words_2 = word_matrix[sent_2]

            # combine the word lists to a set
            word_set = set.union(set(words_1), set(words_2))
            # calculate the numerator
            for word in word_set: 
                numerator += words_1.count(word) * words_2.count(word) * idf[word] ** 2
            # calculate the denominator
            denominator = (sqrt(sentence_denominators[sent_1]) * sqrt(sentence_denominators[sent_2]))
            if denominator == 0:
                idf_cosine = 0
            else:
                idf_cosine = numerator / denominator
                
            # if the sentences are similar enough, set similarity to 1 and increment the sentence degree
            if idf_cosine > threshold:
                similarities[sent_1][sent_2] = 1
                sentence_degree += 1
            else:
                similarities[sent_1][sent_2] = 0

        degrees[sent_1] = sentence_degree

    return similarities, degrees


def power_method(matrix:list, epsilon:int)->list:
    """Applies the power method."""
    p_vector = np.array([1.0 / len(matrix)] * len(matrix))
    lambda_ = 1.0

    while lambda_ > epsilon:
        next_p = np.dot(matrix.T, p_vector)
        lambda_ = np.linalg.norm(np.subtract(next_p, p_vector))
        p_vector = next_p

    return p_vector