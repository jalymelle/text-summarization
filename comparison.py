from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
#from sumy.summarizers.text_rank import TextRankSummarizer as Summarizer
from sumy.summarizers.lex_rank import LexRankSummarizer as Summarizer
from sumy.summarizers.sum_basic import SumBasicSummarizer as Summarizer

LANGUAGE = "english"
SENTENCES_COUNT = 6


if __name__ == "__main__":
    parser = PlaintextParser.from_file(r'data\BBC News Summary\News Articles\business\012.txt', Tokenizer(LANGUAGE))

    summarizer = Summarizer()

    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        print(sentence)