import os
from nltk.tokenize import sent_tokenize, word_tokenize

def get_sentences(doc)->list:
    """Takes a text document and returns a list of all sentences in the document"""
    with open (doc, 'r', encoding='utf-8') as document:
        document = document.read()
        if not document:
            print('Error')
        else:
            sentences = sent_tokenize(document, language='english')
    return sentences



def collect_all_words()->list:
    """returns a set of all the words in the document for each document in the directory"""
    directory = os.path.dirname(os.path.realpath(__file__)) + r'\data\BBC News Summary\News Articles\business'
    all_words = []
    for filename in os.listdir(directory):
        abs_file_path = os.path.join(directory, filename)
        words_in_doc = set()
        with open(abs_file_path, 'r') as document:
            document = document.read()
            if not document:
                print('Error')
            else:
                sentences = sent_tokenize(document, language='english')
            for sentence in sentences:
                words = word_tokenize(sentence)
                for word in words:
                    words_in_doc.add(word)
        all_words.append(words_in_doc)
    
    return all_words
