from brownie import PromissoryNFT, Promissory, accounts

class Promissory:
    def __init__(self, _promissory):
        self.promissory = _promissory
        self.holder = _promissory.promissory()[0]
        self.token_id = _promissory.promissory()[2]

    def set_holder_consent(self, _from):
        self.promissory.setHolderConsent({
            'from': _from,
            'priority_fee': '0.2 gwei'
        })
        print('Holder consent saved!')

    def set_debtor_consent(self, _from):
        self.promissory.setDebtorConsent({
            'from': _from,
            'priority_fee': '0.2 gwei'
        })
        print('Debtor consent saved!')

    # Оплата векселя
    # Требование:
    # - _from == debtor 
    def pay_promissory(self, _debtorAddress):
        self.promissory.payPromissory({
            'from': _debtorAddress,
            'value': '1100 wei',  
            'priority_fee': '10 wei'
        })
        # update_metadata(_from, token_id)
        PromissoryNFT[-1].burnCollectible(self.token_id, {
            'from': self.holder,
            'priority_fee': '10 wei'
        })
        exist = PromissoryNFT[-1].existsCollectible(self.token_id, {
            'from': self.holder,
            'priority_fee': '10 wei'
        })
        assert exist == False
        self.promissory.killContract({
            'from': self.holder,
            'priority_fee': '10 wei'
        })
        return exist

    # Передача токена другому лицу (_to)
    # Требование:
    # - Разрешение распроряжаться токеном (approve) у передающего (owner)
    # - Токен должен сущствовать
    def transfer_token(self, to):
        PromissoryNFT[-1].transferFrom(self.holder, to, self.token_id, {
            'from': self.holder,
            'priority_fee': '10 wei'
        })
        self.promissory.setNewHolder(to, {
            'from': self.holder,
            'priority_fee': '10 wei'
        })