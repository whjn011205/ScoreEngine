from __future__ import print_function # Python 2/3 compatibility
import boto3
from boto3.dynamodb.conditions import Key, Attr
import json
import decimal
import constants as CST




class DynamoUtil: 
    def __init__(self,aws_access_key, aws_secret_key, region):
        self.dynamodb = boto3.resource('dynamodb', aws_access_key_id = aws_access_key, aws_secret_access_key=aws_secret_key, region_name='ap-southeast-1')
    

    def putItem(self, paras):        
        table = self.dynamodb.Table(paras['Table'])
        table.put_item(Item=paras['Item'])
    
    def queryItem(self, paras):
        # paras:
        # {
        #     'Table': '', 
        #     'partitionKey': ('partitionKeyName, 'partitionKeyValue'),
        #     'sortKey':('sortKeyName, ['sortKeyValue1', 'sortKeyValue2'])
        # }
                
        (key, val) = paras['partitionKey']
        keyConiditionExp = Key(key).eq(val)

        if('sortKey' in paras.keys()):
            (key, val) = paras['sortKey']
            if len(val) == 2: 
                keyConiditionExp = keyConiditionExp & Key(key).between(val[0], val[1])
            elif len(val) == 1: 
                keyConiditionExp = keyConiditionExp & Key(key).eq(val[0])
        
        table = self.dynamodb.Table(paras['Table'])
        response = table.query(KeyConditionExpression=keyConiditionExp)
        return response['Items']

    def deleteItem(self, paras):
        # paras:
        # {
        #     'Table': '', 
        #     'partitionKey': ('partitionKeyName, 'partitionKeyValue'),
        #     'sortKey':('sortKeyName, ['sortKeyValue1', 'sortKeyValue2'])
        # }
                
        (key, val) = paras['partitionKey']
        Key = {
            key:val
        }

        if('sortKey' in paras.keys()):
            (key, val) = paras['sortKey']
            Key[key] = val
        
        table = self.dynamodb.Table(paras['Table'])
        table.delete_item(Key=Key)

    def addUser(self, userId, ethAddress):
        paras = {
            'Table': CST.DB_TABLE_USER,
            'Item': {
                CST.DB_USER_ID: userId,
                CST.DB_ETH_ADDRESS: ethAddress
            }
        }
        self.putItem(paras)
    
    def getUser(self, userId):
        paras = {
            'Table': CST.DB_TABLE_USER,
            'partitionKey': ( CST.DB_USER_ID, userId)
        }
        return self.queryItem(paras)

    def addIdentifiedAddress(self, identifiedAddress):
        paras = {
            'Table': CST.DB_TABLE_IDENTIFIED_ADDRESS,
            'Item': self.convertIdentifiedAddressToDynamo(identifiedAddress)            
        }
        self.putItem(paras)

    def convertIdentifiedAddressToDynamo(self, identifiedAddress):
        return {
            CST.DB_CHAIN: identifiedAddress['chain'],
            CST.DB_ADDRESS: identifiedAddress['address'],
            CST.DB_DESCRIPTION: identifiedAddress['description'],
            CST.DB_LINK: identifiedAddress['link'],
            CST.DB_TWITTER: identifiedAddress['twitter']
        }

    def getIdentifiedAddress(self, chain, address):
        paras = {
            'Table': CST.DB_TABLE_IDENTIFIED_ADDRESS,
            'partitionKey': (CST.DB_CHAIN, chain),
            'sortKey':(CST.DB_ADDRESS, [address])
        }
        return self.queryItem(paras)


    def addPendingAddress(self, pendingAddress):
        paras = {
            'Table': CST.DB_TABLE_PENDING_ADDRESS,
            'Item': self.convertPendingAddressToDynamo(pendingAddress)            
        }
        self.putItem(paras)

    def convertPendingAddressToDynamo(self, pendingAddress):
        return {
            CST.DB_USER_ID: pendingAddress['userId'],
            CST.DB_CHAIN: pendingAddress['chain'],
            CST.DB_ADDRESS: pendingAddress['address'],
            CST.DB_DESCRIPTION: pendingAddress['description'],
            CST.DB_LINK: pendingAddress['link'],
            CST.DB_TWITTER: pendingAddress['twitter']
        }

    def getPendingAddress(self, userId):
        paras = {
            'Table': CST.DB_TABLE_PENDING_ADDRESS,
            'partitionKey': (CST.DB_USER_ID, userId),
        }
        return self.queryItem(paras)

    def removePendingAddress(self,userId, address):
        paras = {
            'Table': CST.DB_TABLE_PENDING_ADDRESS,
            'partitionKey': (CST.DB_USER_ID, userId),
            'sortKey': (CST.DB_ADDRESS, address)
        }
        self.deleteItem(paras)

    def addScore(self, score):
        paras = {
            'Table': CST.DB_TABLE_SCORE,
            'Item': self.convertScoreToDynamo(score)
        }
        self.putItem(paras)
    
    def convertScoreToDynamo(self, score):
        return {
            CST.DB_ADDRESS:score['address'],
            CST.DB_VERIFIER_ID: score['verifierId'],
            CST.DB_TIMESTAMP: score['timestamp'],
            CST.DB_SCORE: score['score']
        }
    
    def getScore(self, address):
        paras = {
            'Table': CST.DB_TABLE_SCORE,
            'partitionKey':(CST.DB_ADDRESS, address)
        }
        res = self.queryItem(paras)
        return res