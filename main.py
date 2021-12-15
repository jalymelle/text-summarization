from data import get_sentences, get_words
from algorithms import sumbasic_algorithm, tfidf_algorithm, textrank_algorithm, lexrank_algorithm


def check_sentence_limit(sentence:list, limit:int)->bool:
    "Returns the amount of sentences added. One in each step."
    return 1


def check_word_limit(sentence:list, limit:int)->bool:
    "Returns the amount of words added."
    return len(sentence)
    


def run(text_path:str, algorithm:str, num_sentences=0, num_words=0, ratio=0, category=None)->str:

     # preprocessing: tokenizing into sentences and words
    sentences = get_sentences(text_path)
    words, original_length = get_words(sentences, stem=True, remove_stopwords=True)

    # checking if the user selected any type of limit: either sentence, word or ratio
    if num_sentences != 0 and num_sentences < len(sentences):
        limit_function = check_sentence_limit
        limit = num_sentences

    elif num_words != 0 and num_words < original_length:
        limit_function = check_word_limit
        limit = num_words

    elif ratio != 0:
        limit_function = check_word_limit
        limit = int(ratio * original_length)
    
    else:
        return 'No limit or impossible limit selected'


    if algorithm == 'sumbasic':
        chosen_sentences = sumbasic_algorithm(sentences, words, limit_function, limit)

    elif algorithm == 'tfidf':
        chosen_sentences = tfidf_algorithm(sentences, words, limit_function, limit, category=category)

    elif algorithm == 'textrank':
        chosen_sentences = textrank_algorithm(sentences, words, limit_function, limit,  d=0.85, 
        epsilon=0.001)

    elif algorithm == 'lexrank':
        chosen_sentences = lexrank_algorithm(sentences, words, limit_function, limit, category=category, 
        threshold=0.1, epsilon=0.1)
    
    else:
        return 'No algorithm selected.'
    
    # joining the selected sentences together into a text.
    summary = ' '.join(sentence for sentence in sentences if sentence in chosen_sentences)
    
    return summary


path = r'data\BBC News Summary\News Articles\entertainment\005.txt'

summary_1 = run(path, 'textrank', num_sentences=4)

print(summary_1)