// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

contract Promissory {
    bool public promissoryPaid = false;
    bool public paymentAccepted = false;
    uint256 public dateOfAcceptance;

    //данные векселя хранятся в этой структуре:
    struct PromissoryInfo {
        //Лицо, выдавшее вексель, называется векселедателем.
        //Владеющее векселем – векселедержателем.
        
        address payable holder; //адрес кошелька векселедержателем
        address debtor; //адрес кошелька векселедателя

        uint256 promissoryCommission; //коммисия(в процентах), которая добавится к сумме долга 
        uint256 promissoryAmount; //сумма, нужная должнику
        uint256 dateOfRegistration; //дата составления векселя
        uint256 dateOfClose; //дата погашения векселя
        uint256 dateOfHolderConsent; //дата согласия векселедержателя
        uint256 dateOfDebtorConsent; //дата согласия векселедателя

        bool holderConsent; //согласие векселедержателем
        bool debtorConsent; //согласие векселедателя
    }

    PromissoryInfo private promissory;

    constructor() {
        promissory.holder = payable(msg.sender);
    }

    //записываем информацию по векселю 
    function setPromissoryInfo(
        address payable _debtor,
        uint8 _promissoryCommission,
        uint256 _promissoryAmount,
        uint256 _dateOfClose) public {
            require(_debtor != promissory.holder, "Debtor and Holder must be different persons");
            promissory.debtor = _debtor;
            promissory.promissoryCommission = _promissoryCommission;
            promissory.promissoryAmount = _promissoryAmount + (_promissoryAmount / 100) * promissory.promissoryCommission;
            promissory.dateOfRegistration = block.timestamp;
            promissory.dateOfClose = _dateOfClose;
    }

    //В случае если обе стороны согласны, обозначается дата регистрации векселя
    function setDebtorConsent() public onlyDebtor {
        promissory.debtorConsent = true;
        promissory.dateOfDebtorConsent = block.timestamp;
        if (promissory.holderConsent == true) {
            setDateOfRegistration();
        }
    }

    function setHolderConsent() public onlyHolder {
        promissory.holderConsent = true;
        promissory.dateOfHolderConsent = block.timestamp;
        if (promissory.debtorConsent == true) {
            setDateOfRegistration();
        }
    }

    //обозначение даты регистрации
    function setDateOfRegistration() internal {
        promissory.dateOfRegistration = block.timestamp;
    }

    //оплата векселя
    function payPromissory() public payable onlyDebtor needConsent { 
        address payable debtor = payable(promissory.debtor);
        (bool success,) = debtor.call{value: promissory.promissoryAmount}("");
        require(success, 'Failed call!');
        promissoryPaid = true;
    }

    //Принятие оплаты, что приводит к уничтожению контракта
    //(все еще должна быть функция, которая сжигает токен, когда это делается) 
    function setPaymentAccepted() public onlyHolder promissoryWasPaid {
        require(promissoryPaid == true, "You must pay the amount promissory");
        paymentAccepted = true;
        promissory.dateOfClose = block.timestamp;
        killContract();
    }

    //уничтожение контракта после его заключения
    function killContract() internal onlyHolder {
        selfdestruct(promissory.holder);
    }

    //Получение данных о векселе
    function getPromissoryInfo() external view returns (PromissoryInfo memory) {
        return promissory;
    }
    
    receive() external payable {}

    //модификаторы
    modifier onlyHolder() {
        require(msg.sender == promissory.holder, "Only the Holder!");
        _;
    }

    modifier onlyDebtor() {
        require(msg.sender == promissory.debtor, "Only the Debtor!");
        _;
    }

    modifier needConsent() {
        require(promissory.debtorConsent == true && promissory.holderConsent == true, "Need conset for Holder and Debtor");
        _;
    }

    modifier promissoryWasPaid() {
        require(promissoryPaid == true, "Payment must be made before withdrawing funds!");
        _;
    }
}