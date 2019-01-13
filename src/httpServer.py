from flask import Flask,request
import constants as CST
import pandas as pd
from keys import aws_keys
from dynamoUtil import DynamoUtil 
import etherscan

app = Flask(__name__)

db = DynamoUtil(aws_keys['credentials']['accessKeyId'], aws_keys['credentials']['secretAccessKey'], aws_keys['region'])


def evaluate(addr):
    relatedAddrs = etherscan.getRelatedAddresses(addr)
    dbAddrs = [addr['address'] for addr in db.scanIdentifiedAddress()]

    print('ehterscan related addresses: ',relatedAddrs)
    print('identified scam address in DB: ', dbAddrs)
    dummyScore = 0
    return dummyScore


 
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
