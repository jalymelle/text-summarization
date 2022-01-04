from sys import exit
from string import digits
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, LancasterStemmer

def get_sentences(doc, contains_title:bool)->list:
    """Takes a text document and returns a list of all sentences in the document."""

    # try to read the doucment
    with open (doc, 'r', encoding='utf-8') as document:
        try:
            text = document.read()
        except UnicodeDecodeError:
            exit('Cannot read document. Maybe not a txt file.')
       
        # remove the title because it does not count as a sentence
        if contains_title:
            paragraphs = text.split('\n\n')
            text = ' '.join(paragraphs[1:])
            title = paragraphs[0]
        else:
            title = None
                
        # Split the text into sentences.
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

    for sentence in sentences:
        # split sentence into words
        try:
            words = [word.lower() for word in word_tokenize(sentence)]
        except Exception as e:
                exit('Word Tokenization Error: ' + str(e))

        original_length += len(words)

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
        
        # add word list to word matrix
        word_matrix.append(words)
    
    # in case sentence now contains less than 3 words, remove it (avoid division by 0 error later
    # and if the sentence contains less that two words it is probably not relevant)
    i = 0
    for words in word_matrix:
        if len(words) <= 2:
            word_matrix.remove(words)
            sentences.remove(sentences[i])
        i += 1
    
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