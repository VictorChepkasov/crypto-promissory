from brownie import PromissoryNFT, accounts,Contract

def main():
    set_asks()

def set_asks():
    # Адресс вашего кошелька Metamask
    creator_address = "0xB9a459a00855B0b82337E692D078d7292609701C"
    promissory_collection = PromissoryNFT[-1]

    # Получаем контракты запросов
    asks_address = "0x3634e984Ba0373Cfa178986FD19F03ba4dD8E469"
    asksv1 = Contract.from_explorer(asks_address)
    module_manager = Contract.from_explorer(creator_address)
    erc721_helper_address = creator_address
    promissory_address = "0x96Dc8214D0D9456E4b3182EC4e5cAdcF0004d37e"
    weth_address = "0xd8be3E8A8648c4547F06E607174BAC36f5684756"
    
    holder = accounts.load('victor')

    module_manager.setApprovalForModule(asks_address, True, {"from": holder})
    promissory_collection.setApprovalForAll(erc721_helper_address, True, {"from": holder})

    for token_id in range(100):
        price = (100 - token_id) * 10 ** 16
        asksv1.createAsk(promissory_address, # адрес нашего контракта
                         token_id, # id NFT, который будет указан
                         price, # наша запрашиваемая цена
                         weth_address, # адрес токена, необходимого для оплаты нашего NFT
                         creator_address, # адрес, на который будут отправлены средства
                         0, # награда за поиск
                         {'from': holder}) # подпишите нашу транзакцию с нашей учетной записью