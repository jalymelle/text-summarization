#summary = run('sumbasic', 5)
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.sum_basic import SumBasicSummarizer as Summarizer


LANGUAGE = "english"
SENTENCES_COUNT = 4


if __name__ == "__main__":
    parser = PlaintextParser.from_file(r'data\BBC News Summary\News Articles\business\010.txt', Tokenizer(LANGUAGE))

    summarizer = Summarizer()

    for sentence in summarizer(parser.document, SENTENCES_COUNT):
        print(sentence)