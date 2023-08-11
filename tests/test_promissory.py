import pytest
from brownie import accounts, config, chain
from scripts.promissory_scripts import deploy_promissory, get_promissory_info
from scripts.nft_promissory_scripts import deploy_promissory_nft

@pytest.fixture(scope='session')
def holder():
    return accounts.load('victor')

@pytest.fixture
def promissory(holder):
    return deploy_promissory(holder, accounts.add(config['wallets']['debtor_key']), 10, 2000, 1692126000)

@pytest.fixture
def promissory_nft(holder):
    return deploy_promissory_nft(holder)

def test_deploy(promissory):
    assert promissory.address != '0'

def test_get_promissory_info(holder, promissory):
    info = list(get_promissory_info(holder))
    info[4] //= 3600
    assert info == ['0xB9a459a00855B0b82337E692D078d7292609701C', '0xa5f78F093C1Fa451eAb7D3102AdF1eC6E0b85F27', 10, 2200, chain.time() // 3600, 1692126000, 0, 0, False, False]

