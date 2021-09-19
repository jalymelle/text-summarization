from nltk.tokenize import sent_tokenize
from data import get_sentences
import os
from main import run
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.utils import get_stop_words
#from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
#from sumy.summarizers.sum_basic import SumBasicSummarizer as Summarizer

summaries = []
my_score = 0
sumy_score = 0
total_score = 0

summary_directory = os.path.dirname(os.path.realpath(__file__)) + r'\data\BBC News Summary\Summaries\business'
article_directory = os.path.dirname(os.path.realpath(__file__)) + r'\data\BBC News Summary\News Articles\business'
for filename in os.listdir(article_directory)[0:12]:
    summary_file_path = os.path.join(summary_directory, filename)
    article_file_path = os.path.join(article_directory, filename)
    reference_sentences = get_sentences(summary_file_path)
    length = len(reference_sentences)
    
    with open(article_file_path, 'r', encoding='utf-8') as doc:
        my_summary = run(article_file_path, 'sumbasic', length)
        my_sentences = sent_tokenize(my_summary)
        parser = PlaintextParser.from_file(article_file_path, Tokenizer('english'))
        summarizer = Summarizer()
        summarizer.stop_words = get_stop_words('english')
        sumy_sentences = []
        for sentence in summarizer(parser.document, length):
            sumy_sentences.append(str(sentence))

    for sentence in reference_sentences:
        #print(sentence in my_sentences, sentence in sumy_sentences)
        if sentence in my_sentences:
            my_score += 1
        if sentence in sumy_sentences:
            sumy_score += 1
        total_score += 1
    #print(' ')

print(my_score, sumy_score, total_score)










