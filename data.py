import os
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords

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


def get_words(sentences:list, remove_stopwords:bool)->list:
    """Returns a list of lists. For each sentence, there is a list of 
        all the words in the sentence."""
    word_matrix = []
    for sentence in sentences:
        words = [word.lower() for word in word_tokenize(sentence)]
        if remove_stopwords:
            words = remove_stop_words(words)
    
        word_matrix.append(words)
    return words

def remove_stop_words(words:list)->list:
    "Removes words from the sentence if they are included in the stopwords list."
    stop_words = set(stopwords.words('english'))
    return [word for word in words if word not in stop_words]


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
            words = get_words(sentence, True)
            for word in words:
                words_in_doc.add(word)
        all_words.append(words_in_doc)
    
    return all_words
