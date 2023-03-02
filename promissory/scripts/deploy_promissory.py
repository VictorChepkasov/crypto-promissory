from brownie import Promissory, accounts

def main():
    account = accounts[0]

    promissory_deploy_contract = Promissory.deploy("Victor", {"from":account, "priority_fee":"100 gwei"})
    print(f"Contract deployed at {promissory_deploy_contract}")