import pytest
from conftest import *
from brownie import accounts, chain
from scripts.promissory_scripts import get_promissory_info, pay_promissory, set_debtor_consent, set_holder_consent

# def test_deploy(promissory):
#     assert promissory.address != '0'

# def test_get_promissory_info(holder, promissory):
#     # полчение данных вексселя и обрезание даты до часов
#     info = list(get_promissory_info(holder))
#     info[4] //= 3600
#     assert info == ['0xB9a459a00855B0b82337E692D078d7292609701C', '0xa5f78F093C1Fa451eAb7D3102AdF1eC6E0b85F27', 10, 2200, chain.time() // 3600, 1692126000, 0, 0, False, False]

def test_pay_promissory(holder, debtor, promissory):
    debtorBalance = debtor.balance
    holderBalance = holder.balance
    # стороны дают согласие
    set_debtor_consent(debtor)
    set_holder_consent(holder)
    # оплата векселя
    pay_promissory(debtor)
    promissoryAmount = promissory.promissory().promissoryAmount()
    assert debtorBalance == debtor.balance - promissoryAmount
    assert holderBalance == holder.balance + promissoryAmount