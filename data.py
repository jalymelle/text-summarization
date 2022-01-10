from sys import exit
from string import digits
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, LancasterStemmer


def get_text(path, contains_title, stemmer, stopwords):
    """Returns a list of the sentences and a matrix of the words in the text."""
    text = read_text(path)
    sentences, title = get_sentences(text, contains_title)
    sentences, words, original_length = get_words(sentences, stemmer, stopwords)

    return sentences, words, title, original_length


def read_text(path):
    """Reads a text document"""
    # try to read the document
    with open(path, 'r', encoding='utf-8') as document:
        try:
            text = document.read()
        except UnicodeDecodeError:
            exit('Text file contains characters that cannot be read.')
    
    return text


def get_sentences(text:str, contains_title:bool)->list:
    """Takes a text document and returns a list of all sentences in the document."""
       
    # remove the title because it does not count as a sentence
    if contains_title:
        paragraphs = text.split('\n\n')
        text = ' '.join(paragraphs[1:])
        title = paragraphs[0]
    else:
        title = None
                
    # split the text into sentences
    try:
        sentences = sent_tokenize(text, language='english')
    except Exception as e:
        exit('Sentence Tokenization Error: ' + str(e))

    return sentences, title


def get_words(sentences:list, stem:str, remove_stopwords:bool)->list:
    """Returns a list of lists. For each sentence, there is a list of 
        all the words in the sentence."""

    word_matrix = []
    original_length = 0
    sentences_to_remove = []

    for sentence in sentences:
        # split sentence into words
        try:
            words = [word.lower() for word in word_tokenize(sentence)]
        except Exception as e:
                exit('Word Tokenization Error: ' + str(e))

        # stemming
        if stem == 'p':
            stemmer = PorterStemmer()
            words = [stemmer.stem(word) for word in words]

        elif stem == 'l':
            stemmer = LancasterStemmer()
            words = [stemmer.stem(word) for word in words]

        # remove stop words
        if remove_stopwords:
            words = remove_stop_words(words)
        
    # in case sentence contains more than 3 words, add it (if the sentence contains less than
    # two words it is probably not relevant)
        if len(words) > 3:
            word_matrix.append(words)
            original_length += len(words)
        
        else:
            sentences_to_remove.append(sentence)
    
    for sentence in sentences_to_remove:
        sentences.remove(sentence)

    return sentences, word_matrix, original_length


def remove_stop_words(words:list)->list:
    """Removes words from the sentence if they are included in the NLTK stop words list or the 
        extension of it. Remove digits."""

    remove_numbers = str.maketrans('', '', digits)

    nltk_stop_words = set(stopwords.words('english'))
    exetension_stop_words = set(['.', ',', '!', '?', '\'s', '\'', '"', '[', ']', '(', ')'])
    # combine the NLTK stop words with the exention stop words
    all_stop_words = nltk_stop_words.union(exetension_stop_words)
    
    return [word.translate(remove_numbers) for word in words if word not in all_stop_words]