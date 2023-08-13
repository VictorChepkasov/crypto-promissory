import pytest
from brownie import PromissoryNFT, Promissory, chain
from conftest import *
from scripts.nft_promissory_scripts import get_promissory, create_promissory

def test_nft_promissory_deploy(promissory_nft):
    assert promissory_nft.address != '0'

def test_get_promissory_info(holder, debtor, promissory_id=PromissoryNFT[-1].tokenCounter()):
    create_promissory(holder, debtor, 0, 1000, 1692126000)
    promissory_contract = Promissory.at(get_promissory(holder, promissory_id))
    promissory_info = list(promissory_contract.promissory())
    promissory_info[4] //= 3600
    assert promissory_info == ['0xB9a459a00855B0b82337E692D078d7292609701C', '0xa5f78F093C1Fa451eAb7D3102AdF1eC6E0b85F27', 0, 1000, chain.time() // 3600, 1692126000, 0, 0, False, False]

