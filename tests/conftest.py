import pytest
from brownie import accounts, config
from scripts.promissory_scripts import deploy_promissory
from scripts.nft_promissory_scripts import deploy_promissory_nft

@pytest.fixture(scope='session')
def holder():
    return accounts.load('victor')

@pytest.fixture(scope='session')
def debtor():
    return accounts.load('victor2')

# получение контракта векселя
@pytest.fixture
def promissory(holder, debtor):
    return deploy_promissory(1, holder, debtor, 10, 2000, 1692126000)

# получение фабрики nft
@pytest.fixture
def promissory_nft(holder):
    return deploy_promissory_nft(holder)
