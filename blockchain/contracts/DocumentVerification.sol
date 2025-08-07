// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

/**
 * @title DocumentVerification
 * @dev Smart contract for verifying and tracking document hashes on the blockchain
 */
contract DocumentVerification {
    // Document struct
    struct Document {
        string documentId;         // Unique document ID from backend
        address owner;             // Document owner address
        string documentType;       // Document type (e.g., "financial_statement", "business_plan")
        bytes32 documentHash;      // Hash of the document content
        uint256 timestamp;         // Timestamp when document was added
        bool isVerified;           // Whether the document has been verified
        address verifier;          // Address of the verifier (if verified)
        uint256 verificationDate;  // Timestamp when document was verified
    }

    // State variables
    mapping(bytes32 => Document) public documents;
    mapping(address => bytes32[]) public ownerDocuments;
    
    address public owner;
    mapping(address => bool) public verifiers;

    // Events
    event DocumentAdded(bytes32 indexed docHash, string documentId, address indexed owner, string documentType);
    event DocumentVerified(bytes32 indexed docHash, address indexed verifier);
    event VerifierAdded(address indexed verifier);
    event VerifierRemoved(address indexed verifier);

    // Constructor
    constructor() {
        owner = msg.sender;
        verifiers[msg.sender] = true;
    }

    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    modifier onlyVerifier() {
        require(verifiers[msg.sender], "Only verifiers can call this function");
        _;
    }

    modifier documentExists(bytes32 docHash) {
        require(documents[docHash].owner != address(0), "Document does not exist");
        _;
    }

    // Function to add a new document
    function addDocument(
        string memory _documentId,
        string memory _documentType,
        bytes32 _documentHash
    ) external returns (bytes32) {
        // Generate document hash
        bytes32 docHash = keccak256(abi.encodePacked(_documentId, msg.sender, _documentHash));
        
        // Ensure document doesn't already exist
        require(documents[docHash].owner == address(0), "Document already exists");
        
        // Create document
        Document memory newDocument = Document({
            documentId: _documentId,
            owner: msg.sender,
            documentType: _documentType,
            documentHash: _documentHash,
            timestamp: block.timestamp,
            isVerified: false,
            verifier: address(0),
            verificationDate: 0
        });
        
        // Store document
        documents[docHash] = newDocument;
        
        // Add document to owner mapping
        ownerDocuments[msg.sender].push(docHash);
        
        // Emit event
        emit DocumentAdded(docHash, _documentId, msg.sender, _documentType);
        
        return docHash;
    }

    // Function to verify a document
    function verifyDocument(bytes32 docHash) external onlyVerifier documentExists(docHash) {
        // Get document
        Document storage document = documents[docHash];
        
        // Ensure document is not already verified
        require(!document.isVerified, "Document is already verified");
        
        // Update document
        document.isVerified = true;
        document.verifier = msg.sender;
        document.verificationDate = block.timestamp;
        
        // Emit event
        emit DocumentVerified(docHash, msg.sender);
    }

    // Function to check if a document is verified
    function isDocumentVerified(bytes32 docHash) external view documentExists(docHash) returns (bool) {
        return documents[docHash].isVerified;
    }

    // Function to get document details
    function getDocument(bytes32 docHash) external view documentExists(docHash) returns (
        string memory documentId,
        address documentOwner,
        string memory documentType,
        bytes32 documentHash,
        uint256 timestamp,
        bool isVerified,
        address verifier,
        uint256 verificationDate
    ) {
        Document storage document = documents[docHash];
        
        return (
            document.documentId,
            document.owner,
            document.documentType,
            document.documentHash,
            document.timestamp,
            document.isVerified,
            document.verifier,
            document.verificationDate
        );
    }

    // Function to get documents for an owner
    function getOwnerDocuments(address documentOwner) external view returns (bytes32[] memory) {
        return ownerDocuments[documentOwner];
    }

    // Function to add a verifier
    function addVerifier(address verifier) external onlyOwner {
        require(verifier != address(0), "Invalid verifier address");
        require(!verifiers[verifier], "Address is already a verifier");
        
        verifiers[verifier] = true;
        
        emit VerifierAdded(verifier);
    }

    // Function to remove a verifier
    function removeVerifier(address verifier) external onlyOwner {
        require(verifiers[verifier], "Address is not a verifier");
        require(verifier != owner, "Cannot remove contract owner as verifier");
        
        verifiers[verifier] = false;
        
        emit VerifierRemoved(verifier);
    }

    // Function to check if an address is a verifier
    function isVerifier(address verifier) external view returns (bool) {
        return verifiers[verifier];
    }

    // Function to transfer ownership
    function transferOwnership(address newOwner) external onlyOwner {
        require(newOwner != address(0), "Invalid owner address");
        
        owner = newOwner;
        verifiers[newOwner] = true;
    }
}