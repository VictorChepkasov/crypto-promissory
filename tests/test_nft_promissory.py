import pytest
from brownie import PromissoryNFT, chain
from conftest import *
from scripts.nft_promissory_class import *
from scripts.token_scripts import (
    get_promissory,
    create_promissory,
    approve,
)

def test_nft_promissory_deploy(promissory_nft):
    assert promissory_nft.address != '0'

def test_get_promissory_token_info(holder, debtor, promissory_nft):
    promissory = Promissory(get_promissory(
        holder,
        create_promissory(holder, debtor, 10, 1000, 1693335600)
    ))
    promissory_info = list(promissory.promissory.promissory())
    promissory_info[5] //= 3600
    if network.show_active() != 'development':
        holderAddress = '0xB9a459a00855B0b82337E692D078d7292609701C'
        debtorAddress = '0xa5f78F093C1Fa451eAb7D3102AdF1eC6E0b85F27'
    else:
        holderAddress, debtorAddress = accounts[0], accounts[1]
    assert promissory_info == [holderAddress, debtorAddress, promissory.token_id, 10, 1100, chain.time() // 3600, 1693335600, 0, 0, False, False]

def test_pay_promissory(holder, debtor, promissory_nft):
    promissory = Promissory(get_promissory(
        holder,
        create_promissory(holder, debtor, 10, 1000, 1693335600)
    ))
    promissory.set_holder_consent(holder)
    promissory.set_debtor_consent(debtor)
    exist_token = promissory.pay_promissory(debtor)
    assert exist_token == False

def test_transfer_token(holder, debtor, third_party, promissory_nft):
    promissory = Promissory(get_promissory(
        holder,
        create_promissory(holder, debtor, 10, 1000, 1693335600)
    ))
    # _to - лицо, которому передаётся вексель
    to = third_party if network.show_active() != 'development' else accounts[2]
    approve(holder, PromissoryNFT[-1].address, promissory.token_id)
    promissory.transfer_token(to)
    # получение ненешнего владельца токена векселя
    owner = PromissoryNFT[-1].ownerOf(promissory.token_id, {
        'from': to,
        'priority_fee': '10 wei'
    })
    assert owner == to
    newOwner = get_promissory(to, promissory.token_id).promissory()[0]
    print(f'New Owner: {newOwner}')
    assert newOwner == to