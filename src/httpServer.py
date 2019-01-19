from flask import Flask,request
import constants as CST
import pickle
import pandas as pd
import json
# from keys import aws_keys
# from dynamoUtil import DynamoUtil 
# import etherscan
import random
from scrap import getAddressComments

app = Flask(__name__)

model=None
bow_transformer = None
tfidf_transformer = None
with open('model/model.pickle', 'rb') as f:
    model = pickle.load(f)
with open('model/bow_transformer.pickle', 'rb') as f:
    bow_transformer = pickle.load(f)
with open('model/tfidf_transformer.pickle', 'rb') as f:
    tfidf_transformer = pickle.load(f)

# db = DynamoUtil(aws_keys['credentials']['accessKeyId'], aws_keys['credentials']['secretAccessKey'], aws_keys['region'])

# def text_process(comments):
#     nopunc = [char for char in comments if char not in string.punctuation ]
#     nopunc = ''.join(nopunc)

#     return [word for word in nopunc.split()
#           if word.lower not in stopwords.words('english')
#           and word.lower not in stopwords.words('german')]

def evaluate(addr):
    # relatedAddrs = etherscan.getRelatedAddresses(addr)
    # dbAddrs = [addr['address'] for addr in db.scanIdentifiedAddress()]

    # print('ehterscan related addresses: ',relatedAddrs)
    # print('identified scam address in DB: ', dbAddrs)
    # dummyScore = 0
    comments = getAddressComments(addr)
    X_test =pd.DataFrame([comments])
    test_bow = bow_transformer.transform(X_test['comments'])
    test_tfidf = tfidf_transformer.transform(test_bow)
    vec_test =test_tfidf
    score = model.predict_proba(vec_test)*90
    score = score[0][1]
    
    response = {
        'address':addr,
        'score':score,
        'comments':comments
    }
    return json.dumps(response, indent=4)


 
@app.route("/")
def query():
    score = None
    addr = request.args.get('address').lower()
    if addr is None: 
        score =  None
    else:
        score =  evaluate(addr)

    return str(score)



 
app.run(port=CST.SCORE_ENGINE_HTTP_SERVER_PORT)


# from flask import Flask
# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello World!"

# app.run(port=3001)
