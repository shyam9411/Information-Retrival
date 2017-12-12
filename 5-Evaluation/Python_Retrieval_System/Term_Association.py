
"""
Author: Shihao Wang
There are some functions used to calculate the term association.

"""


# GIVEN: two terms to be compared, top ranking corpus and window size
# RETURN: float, the term association value
def dice_coefficient(term1, term2, top_ranked_corpus, window=-1):
    na, nb, nab = 0, 0, 0
    if window == -1:
        for doc in top_ranked_corpus:
            if term1 in doc and term2 in doc:
                nab += 1
                na += 1
                nb += 1
                continue
            if term1 in doc:
                na += 1
                continue
            if term2 in doc:
                nb += 1
    elif window > 1:
        for doc in top_ranked_corpus:
            start = 0
            while start+window <= len(doc):
                if term1 in doc[start:start+window] and term2 in doc[start:start+window]:
                    nab += 1
                    na += 1
                    nb += 1
                    start += 1
                    continue
                if term1 in doc[start:start+window]:
                    na += 1
                    start += 1
                    continue
                if term2 in doc[start:start+window]:
                    nb += 1
                start += 1
    else:
        return 0
    return float(nab) / (na + nb)


# GIVEN: two terms to be compared, top ranking corpus and window size
# RETURN: float, the term association value
def mutual_information(term1, term2, top_ranked_corpus, window=-1):
    na, nb, nab = 0, 0, 0
    if window == -1:
        for doc in top_ranked_corpus:
            if term1 in doc and term2 in doc:
                nab += 1
                na += 1
                nb += 1
                continue
            if term1 in doc:
                na += 1
                continue
            if term2 in doc:
                nb += 1
    elif window > 1:
        for doc in top_ranked_corpus:
            start = 0
            while start+window <= len(doc):
                if term1 in doc[start:start+window] and term2 in doc[start:start+window]:
                    nab += 1
                    na += 1
                    nb += 1
                    start += 1
                    continue
                if term1 in doc[start:start+window]:
                    na += 1
                    start += 1
                    continue
                if term2 in doc[start:start+window]:
                    nb += 1
                start += 1
    else:
        return 0
    return float(nab) / (na * nb)
