from math import log10
from nltk.tokenize import word_tokenize
from data import collect_all_words

def calculate_word_frequency(sentences)->dict:
    word_frequencies = {}
    num_words = 0
    for sentence in sentences:
        words = word_tokenize(sentence)
        for word in words:
            if word not in word_frequencies:
                word_frequencies[word] = 1
            else: 
                word_frequencies[word] += 1
            num_words += 1

    # Worthäufigkeiten durch Anzahl Wörter teilen
    for frequency in word_frequencies:
        word_frequencies[frequency] = word_frequencies[frequency] / num_words

    return word_frequencies


def calculate_inverse_document_frequency(sentences)->dict:
    all_words = collect_all_words()
    inverse_document_frequencies = {}

    for sentence in sentences:
        words = word_tokenize(sentence)
        for word in words:
            if word not in inverse_document_frequencies:
                num_contain_word = 1
            for word_set in all_words:
                if word in word_set:
                    num_contain_word += 1
            inverse_document_frequencies[word] = log10(len(all_words) / num_contain_word)
    return inverse_document_frequencies


def update_word_frequency(sentence:str, frequency_dict:dict)->dict:
    """Decreases the word probability of the words in the chosen sentence"""
    words = word_tokenize(sentence)
    for word in words:
        frequency_dict[word] = frequency_dict[word] ** 2
    return frequency_dict


def calculate_tfidf(sentences:list)->dict:
    word_frequencies = calculate_word_frequency(sentences)
    inverse_document_frequencies = calculate_inverse_document_frequency(sentences)
    tfidf_scores = {}
    for sentence in sentences:
        words = word_tokenize(sentence)
        for word in words:
            tfidf = word_frequencies[word] * inverse_document_frequencies[word]
            tfidf_scores[word] = tfidf
    
    return tfidf_scores