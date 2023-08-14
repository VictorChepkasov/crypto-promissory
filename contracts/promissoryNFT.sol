// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "../.deps/npm/@openzeppelin/contracts@4.8.1/token/ERC721/ERC721.sol";
import "../.deps/npm/@openzeppelin/contracts@4.8.1/token/ERC721/extensions/ERC721URIStorage.sol";
// import "../.deps/npm/@openzeppelin/contracts@4.8.1/token/ERC721/extensions/ERC721Burnable.sol";
import "./promissory.sol";

contract PromissoryNFT is ERC721URIStorage {
    uint256 public tokenCounter;
    mapping(uint => Promissory) promissories;
    
    constructor() ERC721("Promissory NFT", "PMY") {
        tokenCounter = 0;
    }
    
    /* Требования:
    * - Контракт должен существовать и находиться в мапинге. */
    function getPromissory(uint promissoryId) external view returns(Promissory) {
        require(promissoryId != 0, "The promissory doesn't exist!");
        require(
            promissories[promissoryId].isExist(),
            "The promissory doesn't exist!"
        );
        return promissories[promissoryId];
    }
    /* Требования:
    * - Контракт должен быть утверждённым оператором токена. */
    function payPromissory(uint promissoryId) public payable {
        Promissory promissory = promissories[promissoryId];
        promissory.payPromissory();
        burnCollectible(promissory, promissoryId);
    }

    /* Требования:
    * - _debtor != msg.sender. */
    function createCollectible(
        address payable _debtor,
        uint8 _promissoryCommission,
        uint256 _promissoryAmount,
        uint256 _dateOfClose
    )
        public
    {
        Promissory promissory = new Promissory(
            msg.sender,
            _debtor,
            _promissoryCommission,
            _promissoryAmount,
            _dateOfClose
        );
        tokenCounter += 1;
        promissories[tokenCounter] = promissory;
    }

    /* Требования:
    * - `tokenId` не должен существовать. */
    function mintCollectible(string memory tokenURI) public {
        uint tokenId = tokenCounter;
        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, tokenURI);
    }

    /* Требования:
    * - вызывающий абонент должен владеть токеном или быть утвержденным оператором.
    * - `tokenId` должен существовать. */
    function burnCollectible(
        Promissory promissory,
        uint tokenId
    )
        internal isApprovedOrOwner(tokenId)
    {
        require(promissory.paymentAccepted(), "Payment not accepted!");
        _burn(tokenId);
    }    

    modifier isApprovedOrOwner(uint tokenId) {
        require(
            _isApprovedOrOwner(address(this), tokenId),
            "Caller is not token owner or approved"
        );
        _;
    }
}