// SPDX-License-Identifier: MIT
pragma solidity ^0.8.7;

import "../.deps/npm/@openzeppelin/contracts@4.8.1/token/ERC721/ERC721.sol";
import "../.deps/npm/@openzeppelin/contracts@4.8.1/token/ERC721/extensions/ERC721URIStorage.sol";
import "../.deps/npm/@openzeppelin/contracts@4.8.1/token/ERC721/extensions/ERC721Burnable.sol";
import "../.deps/npm/@openzeppelin/contracts@4.8.1/access/Ownable.sol";
import "../.deps/npm/@openzeppelin/contracts@4.8.1/utils/Counters.sol";

contract PromissoryNFT is ERC721, ERC721URIStorage, ERC721Burnable, Ownable {
    using Counters for Counters.Counter;

    Counters.Counter private _tokenIdCounter;

    constructor() ERC721("PromissoryNFT", "PMY") {}

    function safeMint(address to, string memory uri) public onlyOwner {
        uint256 tokenId = _tokenIdCounter.current();
        _tokenIdCounter.increment();
        _safeMint(to, tokenId);
        _setTokenURI(tokenId, uri);
    }

    // The following functions are overrides required by Solidity.

    function _burn(uint256 tokenId) internal override(ERC721, ERC721URIStorage) {
        super._burn(tokenId);
    }

    function tokenURI(uint256 tokenId)
        public
        view
        override(ERC721, ERC721URIStorage)
        returns (string memory)
    {
        return super.tokenURI(tokenId);
    }
}
