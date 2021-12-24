from main import run
from data import get_sentences

path = r'data\maturaarbeit.txt'

sentences, title = get_sentences(path, contains_title=False)
print(len(sentences))

summary_1 = run(path, 'sumbasic', num_sentences=20, category='all')
summary_2 = run(path, 'tfidf', num_sentences=20, category='all')
summary_3 = run(path, 'textrank', num_sentences=20, category='all')
summary_4 = run(path, 'lexrank', num_sentences=20, category='all')

scores = []

for sentence in sentences:
    score = 0
    if sentence in summary_1:
        score += 1
    if sentence in summary_2:
        score += 1
    if sentence in summary_3:
        score += 1
    if sentence in summary_4:
        score += 1
    scores.append(score)


print(scores)
i = 0
for score in scores:
    if score > 1:
        print(sentences[i])
    i += 1









