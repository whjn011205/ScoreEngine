from dynamoUtil import DynamoUtil
from keys import aws_keys
from datetime import datetime

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
    


def startTest():
    # testAddUser()
    # testGetUser()

    # testAddIdentifiedAddress()
    # testGetIdentifiedAddress()

    # testAddPendingAddress()
    # testGetPendingAddress()
    # testRemovePendingAddress()
    # testGetPendingAddress()

    testAddScore()
    testGetScore()



    



if __name__ == '__main__':
    startTest()
    