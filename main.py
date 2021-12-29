from data import get_sentences, get_words
from algorithms import sumbasic_algorithm, tfidf_algorithm, textrank_algorithm, lexrank_algorithm    


def run(text_path:str, algorithm:str, stemmer='p', stopwords=True, num_sentences=0, num_words=0, 
    percentage=0, category='all', contains_title=False)->str:
    """Checks if all the inputs are valid are calls the algorithm."""
    
    # preprocessing: tokenizing into sentences and words
    sentences, title = get_sentences(text_path, contains_title)
    sentences, words, original_length = get_words(sentences, stemmer, stopwords)


    # check if the user selected any type of limit: either sentence, word or ratio
    # check whether the limit is valid
    if num_sentences != 0 and num_sentences < len(sentences):
        limit_function = check_sentence_limit
        limit = num_sentences

    elif num_words != 0 and num_words < original_length:
        limit_function = check_word_limit
        limit = num_words

    elif percentage != 0:
        limit_function = check_word_limit
        limit = int(percentage * original_length)
    
    else:
        return 'No limit or impossible limit selected'


    # check which algorithm was selected an run it
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
    
    
    # joining the selected sentences together into a text
    summary = ' '.join(sent.replace('\n', ' ') for sent in sentences if sent in chosen_sentences)

    # adding the title again
    if title:
        summary = title + '\n' + summary
    
    return summary


def check_sentence_limit(sentence:list)->bool:
    """Returns the amount of sentences added. One in each step."""
    return 1


def check_word_limit(sentence:list)->bool:
    """Returns the amount of words added."""
    return len(sentence.split())


path = r'data\maturaarbeit.txt'
save_to_file = False

summary = run(path, 'tfidf', num_sentences=4, contains_title=True)

print(summary)

if save_to_file:
    with open(r'lexrank_summary.txt', 'w') as document:
        document.write(summary)
