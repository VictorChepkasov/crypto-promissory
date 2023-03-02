from brownie import PromissoryNFT, accounts

def main():
    account = accounts[0]

    promissoryNFT_deploy_contract = PromissoryNFT.deploy({"from":account, "priority_fee":"150 gwei"})
    print(f"Contract deployed at {promissoryNFT_deploy_contract}")