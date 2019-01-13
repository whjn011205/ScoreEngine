import constants as CST
from keys import etherscan_keys
import requests

apiKey = etherscan_keys['apiKey']

def composeQuery(paras):
    res = []
    for (key,val) in paras.items():
        res.append(key+'='+val)
    res = '&'.join(res)
    return res

def getLatestBlock():
    url = CST.ETHERSCAN_KOVAN_BASEPOINT
    url += 'api?&module=proxy&action=eth_blockNumber'
    r=requests.get(url).json()
    latestBlkNo = int(r['result'],0)
    print(url)
    return latestBlkNo

def getBlockReward():
    pass


def getTxns(address, startBlock = None, endBlock=None):
    url = CST.ETHERSCAN_KOVAN_BASEPOINT
    url += 'api?&module=account&action=txlist&'

    defaultNumBlks = 200000

    chunksize = 10000

    latestBlkNo =  getLatestBlock()
    endBlock = endBlock if endBlock is not None else latestBlkNo
    startBlock = startBlock if startBlock is not None else endBlock - defaultNumBlks
    if startBlock <0:
        startBlock=0
    
    allTxns = []

    start = startBlock
    end = start+chunksize
    while start<endBlock:
        url = CST.ETHERSCAN_KOVAN_BASEPOINT
        url += 'api?&module=account&action=txlist&'
        paras = {
            'address':address,
            'startblock':str(start),
            'endblock':str(end),
            'sort':'desc',
            'apiKey': apiKey
        }
        url+= composeQuery(paras)
        r = requests.get(url).json()
        txns = r['result']
        allTxns+=txns
        print('------------')
        print(start, end)
        print(url)

        start = end+1
        end=start+chunksize
    print(len(allTxns))
    return allTxns

def getRelatedAddresses(addr):
    txns = getTxns(addr)
    relatedAddrs = set([])
    allAddrs = []
    for txn in txns:
        fromAddr = txn['from'].lower()
        toAddr = txn['to'].lower()
        if fromAddr!= addr:
            relatedAddrs.add(fromAddr)
            allAddrs.append(fromAddr)
            print(fromAddr, 'added')
        else: 
            print(fromAddr,'=', addr)
        if toAddr!= addr:
            relatedAddrs.add(toAddr)   
            allAddrs.append(toAddr)

            print(toAddr, 'added')
        else:
            print(toAddr,'=', addr)    

    print('--------',addr,'------------')
    print(len(txns), 'txns')
    print(len(allAddrs))
    print(len(set(allAddrs)))
    return list(relatedAddrs)    
    


if __name__ == '__main__':
    getLatestBlock()
    getTxns('0x895613e730e4F6F850F02b6b51Ea12070b8AD149')



"""
http://api-kovan.etherscan.io/api?module=account&action=txlist&address=0xddbd2b932c763ba5b1b7ae3b362eac3e8d40121a&startblock=0&endblock=99999999&sort=asc&apikey=YourApiKeyToken
"""
"""
https://api.etherscan.io/api?module=proxy&action=eth_blockNumber&apikey=YourApiKeyToken
"""
"""
https://api.etherscan.io/api?module=block&action=getblockreward&blockno=2165403&apikey=YourApiKeyToken
"""