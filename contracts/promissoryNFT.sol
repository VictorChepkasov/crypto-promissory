// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "../.deps/npm/@openzeppelin/contracts@4.8.1/token/ERC721/ERC721.sol";
import "../.deps/npm/@openzeppelin/contracts@4.8.1/token/ERC721/extensions/ERC721URIStorage.sol";

contract PromissoryNFT is ERC721URIStorage {
    uint256 public tokenCounter;
    
    constructor() ERC721("Promissory NFT", "PMY") {
        tokenCounter = 0;
    }

    function mintToken(string memory tokenURI) public returns (bytes32) {
        uint256 tokenId = tokenCounter;
        _safeMint(msg.sender, tokenId);
        _setTokenURI(tokenId, tokenURI);
		tokenCounter++;
    }

    function createCollectible(string memory tokenUri) public returns (uint256) {
        uint256 newTokenId = tokenCounter;
        _safeMint(msg.sender, newTokenId);
        _setTokenURI(newTokenId, tokenUri);
        tokenCounter += 1;
        
        return tokenCounter;
    }
}