from dynamoUtil import DynamoUtil
from keys import aws_keys
from datetime import datetime
import yaml
import json

db = DynamoUtil(aws_keys['credentials']['accessKeyId'], aws_keys['credentials']['secretAccessKey'], aws_keys['region'])

ADDR = '0x1234567'
UID = 'id2'
VF = 'vf2'
SCORE = 92

def testAddUser():
    userId = UID
    ethAddr = ADDR
    db.addUser(userId,ethAddr)

def testGetUser():
    userId = UID
    res = db.getUser(userId)
    print(res)

def testAddIdentifiedAddress():
    identifiedAddress = {
        'chain': 'ETH',
        'address': ADDR,
        'description': 'dummy address',
        'link': 'www.dummyscam.com',
        'twitter':'123456'
    }
    db.addIdentifiedAddress(identifiedAddress)

def testGetIdentifiedAddress():
    chain = 'ETH'
    addr = ADDR
    res = db.getIdentifiedAddress(chain, addr)
    print(res)

def testAddPendingAddress():
    pendingAddress = {
        'userId': UID,
        'chain': 'ETH',
        'address': ADDR,
        'description': 'dummy address',
        'link': 'www.dummyscam.com',
        'twitter':'123456'
    }
    db.addPendingAddress(pendingAddress)

def testGetPendingAddress():
    userId = UID
    res = db.getPendingAddress(userId)
    print(res)

def testRemovePendingAddress():
    userId = UID
    address = ADDR
    db.removePendingAddress(userId, address)

def testAddScore():
    score = {
        'address': ADDR,
        'verifierId': VF,
        'timestamp': int(datetime.utcnow().timestamp()),
        'score': SCORE
    }
    db.addScore(score)

def testGetScore():
    addr = ADDR
    res = db.getScore(addr)
    print(res)  

def testScanIdentifiedAddress():
    res = db.scanIdentifiedAddress()
    print(res)  
    


def startTest():
    # testAddUser()
    # testGetUser()

    # testAddIdentifiedAddress()
    # testGetIdentifiedAddress()
    # testScanIdentifiedAddress()


    # testAddPendingAddress()
    # testGetPendingAddress()
    # testRemovePendingAddress()
    # testGetPendingAddress()

    # testAddScore()
    testGetScore()

if __name__ == '__main__':
    # newY = []
    # f = open('scams.yaml')
    # y = yaml.load(f)
    # # json.dump(y,open('scams.json','w'))
    # for row in y:
    #     if 'addresses' in row.keys():
    #         newY.append(row)
    # json.dump(newY,open('scamAddr.json','w'))


    identifiedAddrs= []
    scams = json.loads(open('scamAddr.json').read())
    for scam in scams[0:5]:
        print(scam)
        addrs = scam['addresses']
        chain = scam['coin']
        if chain!='ETH':
            continue

        link = scam['url'] if 'url' in scam.keys() else ''
        description = {
            'reporter':scam['reporter'],
            'category':scam['category'],
            'subcategory': scam['subcategory'] if 'subcategory' in scam.keys() else 'NA',
            'description':scam['description'] if 'description' in scam.keys() else 'NA'
        }
        for addr in addrs:
            row = {
                'chain':chain,
                'address': addr,
                'link': link,
                'description': json.dumps(description),
                'twitter': 'NA'
            }
            identifiedAddrs.append(row)   
            db.addIdentifiedAddress(row)

    # json.dump(identifiedAddrs, open('identifiedAddrs.json','w'))


    # identifiedAddrs = json.loads(open('identifiedAddrs.json').read())
    # for identifiedAddr in identifiedAddrs:
    #     print(identifiedAddr)



        



    # print(y)
    # # f = open('scams.yaml')
    # # y = yaml.load(f)
    # # print(y)
    # startTest()
    