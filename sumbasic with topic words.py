# TODO: nltk.tokenize to split words

# Dokument einlesen und in Sätze aufteilen und diese Sätze in all_sentences speichern
all_sentences = []

summary_length = 2
selected_words = []
done = False
while not done:
    word = input('What word is important? (Press x to finish.)')
    if word == 'x':
        done = True

with open ('doc.txt', 'r', encoding='utf-8') as document:
    paragraphs = document.readlines()
    for paragraph in paragraphs: 
        sentences = paragraph.split('.')
        for sentence in sentences:
            sentence = sentence.replace('\n', '')
            all_sentences.append(sentence)


# Zählen wie oft jedes Wort vorkommt und diese Häufigkeit in word_frequencies abspeichern
word_frequencies = {}
num_words = 0

for sentence in all_sentences:
    words = sentence.split(' ')
    for word in words:
        if word not in word_frequencies:
            word_frequencies[word] = 1
        else: 
            word_frequencies[word] += 1
        if word in selected_words:
            word_frequencies[word] += 5
        num_words += 1

# Worthäufigkeiten durch Gesamtanzahl Wörter teilen
for frequency in word_frequencies:
    word_frequencies[frequency] = word_frequencies[frequency] / num_words



# Sätzen einen Score geben und den Satz mit dem höchsten Score auswählen bis gewünschte Länge erreicht wird.
# Score = durchschnittliche Wahrscheinlichkeit der Wörter im Satz.
chosen_sentences = []

while len(chosen_sentences) < summary_length:
    sentence_scores = {}

    for sentence in all_sentences:
        sentence_score = 0
        words = sentence.split(' ')
        sentence_length = len(words)
        for word in words:
            frequency = word_frequencies[word]
            sentence_score += frequency / sentence_length
        sentence_scores[sentence] = sentence_score


    # Satz mit höchstem Score auswählen
    best_sentence = max(sentence_scores)
    chosen_sentences.append(best_sentence)
    all_sentences.remove(best_sentence)

    # Worwahrscheinlichkeit der Wörter im Satz verringern, damit nicht zu oft das Gleiche in der Zusammenfassung vorkommt.
    for word in best_sentence.split(' '):
        word_frequencies[word] = word_frequencies[word] ** 2

summary = '. '.join(sentence for sentence in chosen_sentences)
print(summary)