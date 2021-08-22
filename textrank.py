

# Text in Sätze aufteilen


# Gemeinsame Wörter berechnen
# score_out is sum of all weights of sentences that sentence points to.
score_out = []
for i in all_similarities: 
    score_out.append(sum(i))

# nxn matrix of scores, set all scores to 1
sentence_scores = [1 for sentence in vertices]

# mit Formel Score berechnen # get score of vertices by iteratively updating scores

# until convergence:
for score in range(len(sentence_scores)):
    update = 0
    for i in range(len(vertices)):
        common_score = all_similarities[score][i]
        if common_score != 0:
            update += common_score * sentence_scores[i] / score_out[i] 

    updated_score = (1-d) + d * update
    sentence_scores[score-1] = updated_score


# sort vertices based on final score
final_scores = dict(zip(vertices, sentence_scores))

chosen_sentences = []
summary_length = 2

while len(chosen_sentences) < summary_length:
    best_sentence = max(final_scores, key=final_scores.get)
    chosen_sentences.append(best_sentence)
    del final_scores[best_sentence]

summary = '. '.join(sentence for sentence in chosen_sentences)
print(summary)


