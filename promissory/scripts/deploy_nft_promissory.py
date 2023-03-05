from brownie import PromissoryNFT, accounts

def main():
    holder = accounts.load("victor")

    promissoryNFT_deploy_contract = PromissoryNFT.deploy({"from":holder, "priority_fee":"150 gwei"})
    print(f"Contract deployed at {promissoryNFT_deploy_contract}")