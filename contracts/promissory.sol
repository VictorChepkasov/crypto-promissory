// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

contract Promissory {
    bool public paymentAccepted = false; //принята ли оплата
    bool public isExist = false; //существует ли вексель. Обновляется в конструкторе 

    //данные векселя хранятся в этой структуре:
    struct PromissoryInfo {
        //Лицо, выдавшее вексель, называется векселедателем.
        //Владеющее векселем – векселедержателем.
        address payable holder; //адрес кошелька векселедержателем
        address debtor; //адрес кошелька векселедателя
        uint id;
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

    event PaidPromissory(
        uint indexed id,
        uint indexed dateOfClose
    );

    event SetConent(
        uint indexed id,
        uint indexed dateOfRegistration,
        address indexed holder,
        address debtor
    );

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

    constructor(
        uint _id,
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
        isExist = true;
        promissory.id = _id;
        promissory.debtor = _debtor;
        promissory.promissoryCommission = _promissoryCommission;
        promissory.promissoryAmount = _promissoryAmount + (_promissoryAmount / 100) * promissory.promissoryCommission;
        require(promissory.promissoryAmount > 0, "Incorrect promissory amount!");
        promissory.dateOfRegistration = block.timestamp;
        promissory.dateOfClose = _dateOfClose;
    }
    
    receive() external payable {}

    //Получение данных о векселе
    function getPromissoryInfo() external view returns(PromissoryInfo memory) {
        return promissory;
    }

    //оплата векселя
    function payPromissory() public payable onlyDebtor needConsent { 
        address payable holder = payable(promissory.holder);
        require(
            msg.value == promissory.promissoryAmount,
            "Incorrect msg.value!"
        );
        (bool success,) = holder.call{value: msg.value}("");
        require(success, 'Failed call!');
        paymentAccepted = true;
        promissory.dateOfClose = block.timestamp;
        emit PaidPromissory(promissory.id, promissory.dateOfClose);
    }

    //В случае если обе стороны согласны, обозначается дата регистрации векселя
    function setDebtorConsent() public onlyDebtor {
        promissory.debtorConsent = true;
        promissory.dateOfDebtorConsent = block.timestamp;
        if (promissory.holderConsent == true) {
            _setDateOfRegistration();
        }
    }

    function setHolderConsent() public onlyHolder {
        promissory.holderConsent = true;
        promissory.dateOfHolderConsent = block.timestamp;
        if (promissory.debtorConsent == true) {
            _setDateOfRegistration();
        }
    }

    function setNewHolder(address newHolder) public onlyHolder {
        promissory.holder = payable(newHolder);
    }

    //уничтожение контракта после его заключения
    function killContract() public {
        require(paymentAccepted, "Payment don't accepted!");
        isExist = false;
        selfdestruct(promissory.holder);
    }

    //обозначение даты регистрации
    function _setDateOfRegistration() private {
        promissory.dateOfRegistration = block.timestamp;
        emit SetConent(
            promissory.id,
            promissory.dateOfRegistration,
            promissory.holder,
            promissory.debtor
        );
    }
}