import pytest
from brownie import accounts, network
from scripts.promissory_scripts import deploy_promissory
from scripts.nft_promissory_scripts import deploy_promissory_nft

@pytest.fixture(scope='session')
def holder():
    if network.show_active() != 'development':
        return accounts.load('victor')
    else:
        return accounts[0]

@pytest.fixture(scope='session')
def debtor():
    if network.show_active() != 'development':
        return accounts.load('victor2')
    else:
        return accounts[1]

@pytest.fixture(scope='session')
def third_party():
    if network.show_active() != 'development':
        return accounts.load('third_party')
    else:
        return accounts[2]


# получение контракта векселя
@pytest.fixture
def promissory(holder, debtor):
    return deploy_promissory(1, holder, debtor, 10, 2000, 1692126000)

# получение фабрики nft
@pytest.fixture
def promissory_nft(holder):
    return deploy_promissory_nft(holder)
