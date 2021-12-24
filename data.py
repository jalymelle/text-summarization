from string import digits
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer, LancasterStemmer

def get_sentences(doc, contains_title:bool)->list:
    """Takes a text document and returns a list of all sentences in the document."""
    with open (doc, 'r', encoding='utf-8') as document:
        try:
            document = document.read()
        except Exception as e:
            return e
        else:
            # remove the title because it does not count as a sentence
            if contains_title:
                paragraphs = document.split('\n\n')
                document = " ".join(paragraphs[1:])
                title = paragraphs[0]
            else:
                title = None
                
            # Split the text into sentences.
            sentences = sent_tokenize(document, language='english')
    return sentences, title


def get_words(sentences:list, stem:bool, remove_stopwords:bool)->list:
    """Returns a list of lists. For each sentence, there is a list of 
        all the words in the sentence."""
    word_matrix = []
    original_length = 0
    for sentence in sentences:
        words = [word.lower() for word in word_tokenize(sentence)]
        original_length += len(words)
        if stem:
            stemmer = PorterStemmer()
            words = [stemmer.stem(word) for word in words]
        if remove_stopwords:
            words = remove_stop_words(words)
        word_matrix.append(words)
    
    # falls ein Satz nach dem Preprocessing weniger als 3 Wörter enthält, den Satz löschen.
    i = 0
    for words in word_matrix:
        if len(words) <= 2:
            word_matrix.remove(words)
            sentences.remove(sentences[i])
        i += 1
    
            
    return sentences, word_matrix, original_length


def remove_stop_words(words:list)->list:
    "Removes words from the sentence if they are included in the stopwords list."
    remove_numbers = str.maketrans('', '', digits)
    nltk_stop_words = set(stopwords.words('english'))
    other_stop_words = set(['.', ',', '!', '?', '\'s', '\'', '"', '[', ']', '(', ')'])
    all_stop_words = nltk_stop_words.union(other_stop_words)
    
    return [word.translate(remove_numbers) for word in words if word not in all_stop_words]