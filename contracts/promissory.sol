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
        // uint id;
        uint256 promissoryCommission; //коммисия(в процентах), которая добавится к сумме долга 
        uint256 promissoryAmount; //сумма, нужная должнику
        uint256 dateOfRegistration; //дата составления векселя
        uint256 dateOfClose; //дата погашения векселя
        uint256 dateOfHolderConsent; //дата согласия векселедержателя
        uint256 dateOfDebtorConsent; //дата согласия векселедателя
        bool holderConsent; //согласие векселедержателем
        bool debtorConsent; //согласие векселедателя
    }

    PromissoryInfo public promissory;

    constructor(
        address _holder,
        address payable _debtor,
        uint8 _promissoryCommission,
        uint256 _promissoryAmount,
        uint256 _dateOfClose
    ) {
        promissory.holder = payable(_holder);
        require(
            _debtor != promissory.holder, 
            "Debtor and Holder must be different persons"
        );
        promissory.debtor = _debtor;
        promissory.promissoryCommission = _promissoryCommission;
        promissory.promissoryAmount = _promissoryAmount + (_promissoryAmount / 100) * promissory.promissoryCommission;
        promissory.dateOfRegistration = block.timestamp;
        promissory.dateOfClose = _dateOfClose;
    }
    
    receive() external payable {}

    //Получение данных о векселе
    function getPromissoryInfo() external view returns (PromissoryInfo memory) {
        return promissory;
    }

    //оплата векселя
    function payPromissory() public payable onlyDebtor needConsent { 
        address payable holder = payable(promissory.holder);
        (bool success,) = holder.call{value: msg.value}("");
        require(success, 'Failed call!');
        promissoryPaid = true;
        setPaymentAccepted();
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

    //Принятие оплаты, что приводит к уничтожению контракта
    //(все еще должна быть функция, которая сжигает токен, когда это делается) 
    function setPaymentAccepted() internal promissoryWasPaid {
        require(promissoryPaid == true, "You must pay the amount promissory");
        paymentAccepted = true;
        promissory.dateOfClose = block.timestamp;
        killContract();
    }

    //уничтожение контракта после его заключения
    function killContract() internal {
        selfdestruct(promissory.holder);
    }

    //обозначение даты регистрации
    function setDateOfRegistration() private {
        promissory.dateOfRegistration = block.timestamp;
    }

    modifier onlyHolder() {
        require(msg.sender == promissory.holder, "Only the Holder!");
        _;
    }

    modifier onlyDebtor() {
        require(msg.sender == promissory.debtor, "Only the Debtor!");
        _;
    }

    modifier needConsent() {
        require(
            promissory.debtorConsent && promissory.holderConsent,
            "Need conset for Holder and Debtor"
        );
        _;
    }

    modifier promissoryWasPaid() {
        require(
            promissoryPaid, 
            "Payment must be made before withdrawing funds!"
        );
        _;
    }
}