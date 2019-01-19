
import urllib.request
import numpy as np
import random
import re
import os
import time
import bs4 as bs
import pandas as pd
import json

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

df_good = pd.read_json('good_list_withcomments.json')
df_bad = pd.read_json('hack_list_withcomments.json')
# print(df_good.head())
# print(df_bad.head())


common_cols = ['address','commentsCount','comments']
df_good2 = df_good[common_cols]
df_bad2 = df_bad[common_cols]
df = pd.concat([df_good2, df_bad2])
print(len(df_good2), len(df_bad2), len(df))
print(df.head())