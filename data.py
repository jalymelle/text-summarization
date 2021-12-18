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
            
    print(sentences)
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
    return word_matrix, original_length


def remove_stop_words(words:list)->list:
    "Removes words from the sentence if they are included in the stopwords list."
    stop_words = set(stopwords.words('english'))
    return [word for word in words if word not in stop_words]