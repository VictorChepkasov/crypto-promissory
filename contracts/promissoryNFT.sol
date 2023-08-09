// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "../.deps/npm/@openzeppelin/contracts@4.8.1/token/ERC721/ERC721.sol";
import "../.deps/npm/@openzeppelin/contracts@4.8.1/token/ERC721/extensions/ERC721URIStorage.sol";
import "./promissory.sol";

contract PromissoryNFT is ERC721URIStorage {
    uint256 public tokenCounter;
    mapping(uint => Promissory) promissories;
    
    constructor() ERC721("Promissory NFT", "PMY") {
        tokenCounter = 0;
    }

    function createCollectible(
        address payable _debtor,
        uint8 _promissoryCommission,
        uint256 _promissoryAmount,
        uint256 _dateOfClose) public returns(uint256) {
        Promissory promissory = new Promissory();
        promissory.setPromissoryInfo(_debtor, _promissoryCommission, _promissoryAmount, _dateOfClose);
        
        tokenCounter += 1;
        promissories[tokenCounter] = promissory;
        
        return tokenCounter;
    }

    function mintCollectible(string memory tokenURI) public {
        uint tokenId = tokenCounter;
        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, tokenURI);
    } 

    function getPromissoryInfo(uint promissoryId) public view returns(Promissory.PromissoryInfo memory) {
        // тут должна быть проверка на наличие контракта под определённым id
        return promissories[promissoryId].getPromissoryInfo();
    }
}