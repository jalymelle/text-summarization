import os

from nltk.tokenize import word_tokenize
from data import get_sentences, get_words



def collect_all_words()->list:
    """Returns a set of all the words in the document for each document in the directory"""
    directory = os.path.dirname(os.path.realpath(__file__)) + r'\data\BBC News Summary\News Articles\tech'
    directories = [os.path.dirname(os.path.realpath(__file__)) + r'\data\BBC News Summary\News Articles\tech',
    os.path.dirname(os.path.realpath(__file__)) + r'\data\BBC News Summary\News Articles\sport',
    os.path.dirname(os.path.realpath(__file__)) + r'\data\BBC News Summary\News Articles\entertainment',
    os.path.dirname(os.path.realpath(__file__)) + r'\data\BBC News Summary\News Articles\politics',
    os.path.dirname(os.path.realpath(__file__)) + r'\data\BBC News Summary\News Articles\business']
    # All_words is a list of word sets for each document.
    all_words = []
    for directory in directories:
    # Loop over all documents in the directory.
        for filename in os.listdir(directory):
            abs_file_path = os.path.join(directory, filename)
            print(abs_file_path)
            words_in_doc = set()

            # Add all words in the document to words_in_doc.
            sentences = get_sentences(abs_file_path)
            word_matrix, original_length = get_words(sentences, False, False)
            for words in word_matrix:
                for word in words:
                    words_in_doc.add(word)
            all_words.append(words_in_doc)
    
    return all_words

document_word_sets = collect_all_words()
all_words_with_frequencies = {}

for document_word_set in document_word_sets:
    for word in document_word_set:
        if word not in all_words_with_frequencies:
            all_words_with_frequencies[word] = 1
        else: 
            all_words_with_frequencies[word] += 1

with open(r'data\BBC News Summary\idf\all_idf.txt', 'w') as document:
    document.write(str(all_words_with_frequencies))