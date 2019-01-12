from flask import Flask,request
import constants as CST
import pandas as pd
from keys import aws_keys
from dynamoUtil import DynamoUtil 

app = Flask(__name__)

db = DynamoUtil(aws_keys['credentials']['accessKeyId'], aws_keys['credentials']['secretAccessKey'], aws_keys['region'])


def evaluate(addr = ''):
    if addr is None:
        addr = ''
    print(addr)
    print(db.getIdentifiedAddress('ETH',addr))
    return 0
 
@app.route("/")
def query():
    score = None
    addr = request.args.get('address')
    if addr is None: 
        addr = '123'
    score = evaluate(addr)

    return str(score)



 
app.run(port=CST.SCORE_ENGINE_HTTP_SERVER_PORT)


# from flask import Flask
# app = Flask(__name__)

# @app.route("/")
# def hello():
#     return "Hello World!"

# app.run(port=3001)
