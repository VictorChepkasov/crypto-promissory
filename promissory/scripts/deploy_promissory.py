from brownie import Promissory, accounts
# from scripts.createjson import createMetadata
from dotenv import load_dotenv

load_dotenv()

holder = accounts.load("victor")

def deploy_contract():
    promissory_deploy_contract = Promissory.deploy({'from': holder, 'priority_fee': '1 wei'})
    print(f'contract deployed at {promissory_deploy_contract}')
    
    return promissory_deploy_contract

def getPromissoryInfoArr():
    deployed_contract = deploy_contract()
    promissory_info = deployed_contract.getPromissoryInfo({'from': holder})

    #clean promissory info
    chars = "()''"
    promissory_info = str(promissory_info).translate(str.maketrans('', '', chars))

    return promissory_info

def main():
    promissoryInfoArr = getPromissoryInfoArr().split(', ')

    # print promissory info
    print('Holder address:', promissoryInfoArr[0])
    print('Debtor address:', promissoryInfoArr[1])
    print('Commission:', promissoryInfoArr[2])
    print('Amount:', promissoryInfoArr[3])
    print('Date of registration:', promissoryInfoArr[4])
    print('Date of close:', promissoryInfoArr[5])
    print('Date of holder Consent:', promissoryInfoArr[6])
    print('Date of debtor Consent:', promissoryInfoArr[7])
    print('Holder consent:', promissoryInfoArr[8])
    print('Debtor consent:', promissoryInfoArr[9])

    # createMetadata(promissoryInfoArr)