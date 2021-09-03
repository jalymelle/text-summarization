import os
from nltk.tokenize import sent_tokenize, word_tokenize

def get_sentences(doc)->list:
    """Takes a text document and returns a list of all sentences in the document."""
    with open (doc, 'r', encoding='utf-8') as document:
        document = document.read()
        if not document:
            print('Error')
        else:
            # Split the text into sentences.
            sentences = sent_tokenize(document, language='english')
    return sentences


def get_words(sentence:str)->list:
    words = [word.lower() for word in word_tokenize(sentence)]
    return words



def collect_all_words()->list:
    """Returns a set of all the words in the document for each document in the directory"""
    directory = os.path.dirname(os.path.realpath(__file__)) + r'\data\BBC News Summary\News Articles\business'

    # All_words is a list of word sets for each document.
    all_words = []

    # Loop over all documents in the directory.
    for filename in os.listdir(directory):
        abs_file_path = os.path.join(directory, filename)
        words_in_doc = set()

        # Add all words in the document to words_in_doc.
        sentences = get_sentences(abs_file_path)
        for sentence in sentences:
            words = get_words(sentence)
            for word in words:
                words_in_doc.add(word)
        all_words.append(words_in_doc)
    
    return all_words
