import pandas as pd

from querying_identifiied import network_calculated_score
from querying_unidentfied import is_present
from text_scoring import text_based_scoring
from statistics import mean

search_address = input('Enter the address:')

# In Primary database
# search_address = 0x40b9b889a21ff1534d018d71dc406122ebcf3f5a
# Not in primary database
# search_address = 0x04786aada9deea2150deab7b3b8911c309f5ed90


# Read the files
verified_score = pd.read_csv("verified_score.csv")
text_file = pd.read_csv("text.csv")
etherscan_data = pd.read_csv("etherscan_hack1.csv")

# Step 1: Search the verified_score database
# unique score for unique address.

################
# Text Scoring #
################

# Scoring for the keywords
# Negative scoring based on keywords

score_80 = ['stolen', 'hacked', 'hack', 'scammer']
score_90 = ['hiest', 'phish']
score_50 = ['wrong', 'back', 'report']

# Positive scoring based on account activity.
score = []
text_column = text_file[text_file['address'] == search_address]
text = text_column['text']


# After learning the relationship between the verified_score and the text comments,
# the algorithm will issue some scores to the keywords.


def yay_score(_address):
    is_match = verified_score['address'] == _address
    vs = verified_score[is_match]
    return vs['weighted_score']


# yay_score('0x40b9b889a21ff1534d018d71dc406122ebcf3f5a')

# Step 1: Search primary database
if any(verified_score['address'].isin([search_address])):
    score = yay_score(search_address)
else:
    # Step 2: Search if it a recipient address in etherscan database
    if is_present([search_address]) == 1:
        score = network_calculated_score(search_address, etherscan_data, verified_score)
    else:
        text = text_file[text_file['address'] == search_address]
        score = text_based_scoring(text)

print('Score', score)

# Positive scoring based on account activity.
