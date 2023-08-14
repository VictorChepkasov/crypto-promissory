import pytest
from brownie import PromissoryNFT, Promissory, chain
from conftest import *
from scripts.promissory_scripts import set_debtor_consent, set_holder_consent
from scripts.nft_promissory_scripts import (
    get_promissory,
    create_promissory,
    pay_promissory,
    approve,
    transfer_token
)

def test_nft_promissory_deploy(promissory_nft):
    assert promissory_nft.address != '0'

def test_get_promissory_token_info(holder, debtor, promissory_nft):
    create_promissory(holder, debtor, 0, 1000, 1692126000)
    promissory_contract = Promissory.at(get_promissory(
        holder, PromissoryNFT[-1].tokenCounter()
    ))
    promissory_info = list(promissory_contract.promissory())
    promissory_info[5] //= 3600
    if network.show_active() != 'development':
        holderAddress = '0xB9a459a00855B0b82337E692D078d7292609701C'
        debtorAddress = '0xa5f78F093C1Fa451eAb7D3102AdF1eC6E0b85F27'
    else:
        holderAddress, debtorAddress = accounts[0], accounts[1]
    assert promissory_info == [holderAddress, debtorAddress, PromissoryNFT[-1].tokenCounter(), 0, 1000, chain.time() // 3600, 1692126000, 0, 0, False, False]

def test_pay_promissory(holder, debtor, promissory_nft):
    create_promissory(holder, debtor, 10, 1000, 1692126000)
    set_debtor_consent(debtor)
    set_holder_consent(holder)
    token_id = PromissoryNFT[-1].tokenCounter()
    promissory = Promissory.at(get_promissory(debtor, token_id))
    exist_token = pay_promissory(promissory, debtor, token_id)
    assert exist_token == False

def test_transfer_token(holder, debtor, third_party, promissory_nft):
    create_promissory(holder, debtor, 10, 1000, 1692126000)
    token_id = PromissoryNFT[-1].tokenCounter()
    to = third_party if network.show_active() != 'development' else accounts[2]
    approve(holder, PromissoryNFT[-1].address, token_id)
    transfer_token(holder, to, token_id)
    owner = PromissoryNFT[-1].ownerOf(token_id, {
        'from': to,
        'priority_fee': '10 wei'
    })
    assert owner == to

def test_burn_collectible(holder, debtor, promissory_nft):
    create_promissory(holder, debtor, 10, 1000, 1692126000)
    token_id = PromissoryNFT[-1].tokenCounter()
    approve(holder, PromissoryNFT[-1].address, token_id)
    PromissoryNFT[-1].burnCollectible(token_id, {
        'from': holder,
        'priority_fee': '10 wei'
    })
    exist_token = PromissoryNFT[-1].existsCollectible(token_id, {
        'from': holder,
        'priority_fee': '10 wei'
    })
    assert exist_token == False