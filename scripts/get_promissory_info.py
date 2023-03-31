from brownie import accounts, Promissory
from .deploy_promissory import *

promissory_info = promissory_deploy_contract.getPromissoryInfo({'from':account})