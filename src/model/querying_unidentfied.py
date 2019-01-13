""" it will query the files from etherscan database """
import pandas as pd

etherscan_data = pd.read_csv("etherscan_hack1.csv")


def is_present(search_address):
    var1 = etherscan_data['To'].isin(search_address).any
    var2 = etherscan_data['To'].isin(search_address).any
    if var1 or var2:
        return 1
    else:
        return 0

#
#
#
# print(etherscan_data['From'].isin(search_address))
# var = etherscan_data['From'].isin(search_address).any = True
# print(var)
