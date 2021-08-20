from math import sqrt
import numpy as np
from functions import calculate_inverse_document_frequency, get_sentences


threshold = 0.1
epsilon = 0.1

# Text in Sätze aufteilen
vertices = get_sentences('doc.txt')



inverse_document_frequencies = calculate_inverse_document_frequency(vertices)

# create matrix of cosine similarities
sentence_denominators = []

for sentence in vertices:
    sentence_tfidf = 0 
    sentence_split = sentence.split(' ')
    words = set(word for word in sentence_split)
    for word in words:
        tf = sentence_split.count(word)
        sentence_tfidf += tf * inverse_document_frequencies[word] ** 2
    sentence_denominators.append(sentence_tfidf)
    
matrix = np.zeros((len(vertices), len(vertices)))
degrees = []

for i in range(len(vertices)):
    sentence_degree = 1
    sentence_1 = vertices[i].split(' ')
    words = set(word for word in sentence_1)
    for j in range(len(vertices)):
        numerator = 0
        sentence_2 = vertices[j].split(' ')
        words.add(word for word in sentence_2)
        for word in words: 
            numerator += sentence_1.count(word) * sentence_2.count(word) 

        idf_cosine = numerator / (sqrt(sentence_denominators[i]) * sqrt(sentence_denominators[j]))
        if idf_cosine > threshold:
            matrix[i][j] = 1
            sentence_degree += 1
        else:
            matrix[i][j]
    degrees.append(sentence_degree)

    
for i in range(len(vertices)):
    for j in range(len(vertices)):
        matrix[i][j] /= degrees[i]


# mit Hilfe
p_vector = np.array([1.0 / len(vertices)] * len(vertices))
lambda_ = 1.0

while lambda_ > epsilon:
    next_p = np.dot(matrix.T, p_vector)
    lambda_ = np.linalg.norm(np.subtract(next_p, p_vector))
    p_vector = next_p 

final_scores = dict(zip(vertices, p_vector))
chosen_sentences = []
summary_length = 2

while len(chosen_sentences) < summary_length:
    best_sentence = max(final_scores, key=final_scores.get)
    chosen_sentences.append(best_sentence)
    del final_scores[best_sentence]

summary = '. '.join(sentence for sentence in chosen_sentences)
print(summary)
