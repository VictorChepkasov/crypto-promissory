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

    receive() external payable {}
    
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
            tokenCounter+1,
            msg.sender,
            _debtor,
            _promissoryCommission,
            _promissoryAmount,
            _dateOfClose
        );
        tokenCounter += 1;
        promissories[tokenCounter] = promissory;
    }

    // Можно запихнуть createCollectible в эту функцию, так будет надёжнее
    /* Требования:
    * - `tokenId` не должен существовать. */
    function mintCollectible(string memory tokenURI) public {
        uint tokenId = tokenCounter;
        (address holder,,,,,,,,,,) = promissories[tokenId].promissory();
        require(msg.sender == holder, 'Only Holder!');
        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, tokenURI);
    }

    function burnCollectible(uint tokenId) public {
        require(promissories[tokenId].paymentAccepted(), "Payment don't accepted!");
        _burn(tokenId);
    }

    function existsCollectible(uint tokenId) public view returns(bool) {
        return _exists(tokenId);
    }
}