from nltk.tokenize import sent_tokenize
from main import run
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
#from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
#from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer as Summarizer

article_path = r'data\BBC News Summary\News Articles\business\012.txt'
human_summary = r'data\BBC News Summary\Summaries\business\012.txt'

with open (human_summary, 'r') as doc:
    reference_summary = doc.read()
    reference_sentences = sent_tokenize(reference_summary)


length = len(reference_sentences)

generated_summary = run(article_path, 'lexrank', length)
generated_sentences = sent_tokenize(generated_summary)

LANGUAGE = "english"

parser = PlaintextParser.from_file(article_path, Tokenizer(LANGUAGE))
summarizer = Summarizer()
for sentence in summarizer(parser.document, length):
        print(str(sentence) in reference_sentences)


print(length)
for sentence in generated_sentences:
    print(sentence in reference_sentences)








