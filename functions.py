from nltk.tokenize import sent_tokenize

def get_sentences(doc):
    """takes a text document and returns a list of all sentences in the documnent"""
    with open (doc, 'r', encoding='utf-8') as document:
        sentences = sent_tokenize(document, language='english')
    return sentences