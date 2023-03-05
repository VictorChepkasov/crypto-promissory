from brownie import Promissory, accounts
from scripts.createjson import createMetadata

holder = accounts.load("victor")

def deploy_contract():
    promissory_deploy_contract = Promissory.deploy('Victor', {'from': holder, 'priority_fee': '1 wei'})
    print(f'contract deployed at {promissory_deploy_contract}')
    
    return promissory_deploy_contract

def getPromissoryInfoArr():
    promissory_info = deploy_contract().getPromissoryInfo({'from': holder})

    #clean promissory info
    promissory_info = str(promissory_info).replace('(', '')
    chars = "()''"
    promissory_info = promissory_info.translate(str.maketrans('', '', chars))

    return promissory_info

def main():
    promissoryInfoArr = getPromissoryInfoArr().split(', ')

    # print promissory info
    print('Holder address:', promissoryInfoArr[0])
    print('Debtor address:', promissoryInfoArr[1])
    print('Holder name:', promissoryInfoArr[2])
    print('Debtor name:', promissoryInfoArr[3])
    print('Commission:', promissoryInfoArr[4])
    print('Amount:', promissoryInfoArr[5])
    print('Date of registration:', promissoryInfoArr[6])
    print('Date of close:', promissoryInfoArr[7])
    print('Date of holder Consent:', promissoryInfoArr[8])
    print('Date of debtor Consent:', promissoryInfoArr[9])
    print('Holder consent:', promissoryInfoArr[10])
    print('Debtor consent:', promissoryInfoArr[11])

    createMetadata(promissoryInfoArr)
