from brownie import WaterCollection, accounts, config, Contract

def main():
    # Адресс вашего кошелька Metamask
    creator_address = "0xB9a459a00855B0b82337E692D078d7292609701C"
    water_collection = WaterCollection[-1]
    
    # Получаем контракты запросов
    asks_address = "0xA98D3729265C88c5b3f861a0c501622750fF4806"
    asksv1 = Contract.from_explorer(asks_address)
    module_manager = Contract.from_explorer("0xa248736d3b73A231D95A5F99965857ebbBD42D85")
    erc721_helper_address = "0x029AA5a949C9C90916729D50537062cb73b5Ac92"
    water_address = "0xFA3D765E90b3FBE91A3AaffF1a611654B911EADb"
    weth_address = "0xc778417E063141139Fce010982780140Aa0cD5Ab"

    dev = accounts.add(config['wallets']['from_key'])
    
    # Дайте Zora разрешение на проведение транзакций с контрактом ASK
    module_manager.setApprovalForModule(asks_address, True, {"from": dev})
    water_collection.setApprovalForAll(erc721_helper_address, True, {"from": dev})
    
    for token_id in range(100):
        price = (100 - token_id) * 10 ** 16
        asksv1.createAsk(water_address, # адрес нашего контракта
                         token_id, # id NFT, который будет указан
                         price, # наша запрашиваемая цена
                         weth_address, # адрес токена, необходимого для оплаты нашего NFT
                         creator_address, # адрес, на который будут отправлены средства
                         0, # награда за поиск
                         {'from': dev}) # подпишите нашу транзакцию с нашей учетной записью