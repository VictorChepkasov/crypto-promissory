// SPDX-License-Identifier: MIT
pragma solidity 0.8.9;

contract Wechsel {
    uint8 interest_rate; //процентная ставка
    uint256 amount_payable; //сумма к оплате

    string wechsel_type; //простой или переводной вексель
    string wechsel_validity; //срок векселя

    address public debtors_address; //кошелёк должника
    address public buyers_address; //кошелёк покупателя

    //массив адресов должников, через которых прошёл вексель
    address[] public arr_debtors;
}