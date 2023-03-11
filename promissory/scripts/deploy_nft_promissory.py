from brownie import PromissoryNFT, accounts, config

def main():
    holder = accounts.add(config['wallets']['from_key'])

    promissoryNFT_deploy_contract = PromissoryNFT.deploy({"from":holder, "gas_price":"1 gwei"})
    print(f"Contract deployed at {promissoryNFT_deploy_contract}")