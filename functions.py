import os
from nltk.tokenize import sent_tokenize, word_tokenize

def get_sentences(doc):
    """Takes a text document and returns a list of all sentences in the document"""
    with open (doc, 'r', encoding='utf-8') as document:
        sentences = sent_tokenize(document, language='english')
    return sentences


def calculate_word_frequency(sentences):
    """Calculates how often a word is in the tex"""
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

    # Worthäufigkeiten durch Gesamtanzahl Wörter teilen
    for frequency in word_frequencies:
        word_frequencies[frequency] = word_frequencies[frequency] / num_words

    return word_frequencies





def collect_all_words():
    directory = r'C:\Users\megan\Desktop\maturaarbeit\code\data\BBC News Summary\News Articles\business'
    all_words = []
    for filename in os.listdir(directory):
        abs_file_path = os.path.join(directory, filename)
        words_in_doc = set()
        with open(abs_file_path, 'r') as document:
            sentences = sent_tokenize(document, language='english')
            for sentence in sentences:
                words = word_tokenize(sentence)
                for word in words:
                    words_in_doc.add(word)
        all_words.append(words_in_doc)
    
    return all_words