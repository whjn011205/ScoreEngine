import pandas as pd
from statistics import mean

# Scoring for the keywords
# Negative scoring based on keywords

score_80 = ['stolen', 'hacked', 'hack', 'scammer', 'scam']
score_90 = ['hiest', 'phish']
score_50 = ['wrong', 'back', 'report']

score = []


def text_based_scoring(_text):
    # find the length of the text.
    for word in _text:
        if word in score_90:
            score.append(90)
        elif word in score_80:
            score.append(80)
        elif word in score_50:
            score.append(50)
        else:
            continue
    return mean(score)


# _txt = 'This is a scam'
# _txt = _txt.split()
# sd = text_based_scoring(_txt)
# print(sd)
