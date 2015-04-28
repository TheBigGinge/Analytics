import nltk


def jaccard_index(string_1, string_2):
    
    bigram1 = list(nltk.bigrams(string_1.lower()))
    bigram2 = list(nltk.bigrams(string_2.lower()))
    
    union = bigram1 + bigram2

    intersect = 0
    
    for Set in union:
        if Set in bigram1 and Set in bigram2:
            intersect += 1
        else:
            continue
    
    jaccard = float(intersect) / float(len(union))
    
    return jaccard