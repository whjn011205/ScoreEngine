import numpy as np
""" Gives score to the search addresses based on its network of accounts. """

# Hypothesis 1: the higher the amount of money transferred to the account, greater the chances.
# if the transaction fee is the same, then also added score. same person.
#  percentage of hack accounts relation >= 50 %, then suspicious.
# Special emphasis on From/ To transactions.
# Provide screenshots of the types of accounts.
# Recipient address :" 0x04786aada9deea2150deab7b3b8911c309f5ed90 " but unclassified.
# Search etherscan,about this address.
# transactions in the account by the hacker tagged account. '0x40b9b889a21ff1534d018d71dc406122ebcf3f5a'
# Criteria 1
# search_address = '0x04786aada9deea2150deab7b3b8911c309f5ed90'


def network_calculated_score(search_address, etherscan_data, verified_score):
    money_in_score = []
    # Get the etherscan data regarding the unidentified_address
    # etherscan_data = pd.read_csv("etherscan_hack1.csv")
    # verified_score = pd.read_csv("verified_score.csv")

    # Make a dataframe containing transactions into the account
    to_account = etherscan_data['To'] == search_address
    to_search_address_df = etherscan_data[to_account]  # df associated with to search account. User entry.
    total_value_in = sum(to_search_address_df['Value_IN(ETH)'])

    if verified_score['address'].isin(to_search_address_df['From']).any:
        # Identify money coming in from hacked account.
        # write here.
        # create a dataframe
        sent_from_suspicious = etherscan_data.loc[etherscan_data['From'].isin(verified_score['address'])]
        suspicious_value_in = sum(sent_from_suspicious['Value_IN(ETH)'])
        ratio = suspicious_value_in / total_value_in

        if ratio >= 0.90:
            money_in_score.append(100)
        elif 0.90 > ratio >= 0.70:
            money_in_score.append(80)
        elif 0.70 > ratio >= 0.50:
            money_in_score.append(50)

    matches = np.sum(to_search_address_df['From'].isin(verified_score['address']))
    frac_matches = matches / len(to_search_address_df['From'])

    match_score = []
    if frac_matches >= 0.50:
        match_score.append(90)
    elif 0.50 > frac_matches >= 0.30:
        match_score.append(60)
    else:
        match_score.append(0)
        # have t fix if it is zero , then the average will be affected.

    score = np.average([money_in_score[-1], match_score[-1]])
    return score

# Todo: why brackets are need outside?






# scoring based on relation with hacked address.
# SCORING #
# 1. No: of hacked account relations
# 2. Amount of money sent to hacked accounts.
# 3. Transaction fee.
# scoring based on relation with hacked address.
# Get the value in from identified hacked address.