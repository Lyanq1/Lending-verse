// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

import "./LoanAgreement.sol";

/**
 * @title LendingMarket
 * @dev Smart contract for managing the P2P lending marketplace
 */
contract LendingMarket {
    // Loan offer struct
    struct LoanOffer {
        string offerId;            // Unique offer ID from backend
        address payable lender;    // Lender address
        uint256 amount;            // Maximum amount willing to lend
        uint256 minAmount;         // Minimum amount willing to lend
        uint256 interestRate;      // Annual interest rate (in basis points, e.g., 500 = 5%)
        uint256 minTerm;           // Minimum loan term in months
        uint256 maxTerm;           // Maximum loan term in months
        uint256 expiryDate;        // Expiry date timestamp
        bool isActive;             // Whether the offer is active
        string metadataHash;       // IPFS hash for additional offer metadata
    }

    // Loan request struct
    struct LoanRequest {
        string requestId;          // Unique request ID from backend
        address payable borrower;  // Borrower address
        uint256 amount;            // Requested loan amount
        uint256 interestRate;      // Maximum interest rate willing to pay (in basis points)
        uint256 term;              // Requested loan term in months
        uint256 expiryDate;        // Expiry date timestamp
        bool isActive;             // Whether the request is active
        string purpose;            // Purpose of the loan
        string metadataHash;       // IPFS hash for additional request metadata
    }

    // State variables
    mapping(bytes32 => LoanOffer) public loanOffers;
    mapping(bytes32 => LoanRequest) public loanRequests;
    mapping(address => bytes32[]) public lenderOffers;
    mapping(address => bytes32[]) public borrowerRequests;
    
    LoanAgreement public loanAgreementContract;
    address public owner;
    uint256 public platformFeePercent; // Platform fee in basis points (e.g., 100 = 1%)

    // Events
    event LoanOfferCreated(bytes32 indexed offerHash, string offerId, address lender, uint256 amount, uint256 interestRate);
    event LoanOfferUpdated(bytes32 indexed offerHash, uint256 amount, uint256 interestRate);
    event LoanOfferCancelled(bytes32 indexed offerHash);
    event LoanRequestCreated(bytes32 indexed requestHash, string requestId, address borrower, uint256 amount, uint256 interestRate);
    event LoanRequestUpdated(bytes32 indexed requestHash, uint256 amount, uint256 interestRate);
    event LoanRequestCancelled(bytes32 indexed requestHash);
    event LoanAgreementCreated(bytes32 indexed offerHash, bytes32 indexed requestHash, bytes32 loanHash);

    // Constructor
    constructor(address _loanAgreementAddress, uint256 _platformFeePercent) {
        loanAgreementContract = LoanAgreement(_loanAgreementAddress);
        owner = msg.sender;
        platformFeePercent = _platformFeePercent;
    }

    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    modifier onlyLender(bytes32 offerHash) {
        require(msg.sender == loanOffers[offerHash].lender, "Only lender can call this function");
        _;
    }

    modifier onlyBorrower(bytes32 requestHash) {
        require(msg.sender == loanRequests[requestHash].borrower, "Only borrower can call this function");
        _;
    }

    modifier offerExists(bytes32 offerHash) {
        require(loanOffers[offerHash].lender != address(0), "Loan offer does not exist");
        _;
    }

    modifier requestExists(bytes32 requestHash) {
        require(loanRequests[requestHash].borrower != address(0), "Loan request does not exist");
        _;
    }

    // Function to create a new loan offer
    function createLoanOffer(
        string memory _offerId,
        uint256 _amount,
        uint256 _minAmount,
        uint256 _interestRate,
        uint256 _minTerm,
        uint256 _maxTerm,
        uint256 _expiryDate,
        string memory _metadataHash
    ) external returns (bytes32) {
        // Validate inputs
        require(_amount > 0, "Amount must be greater than 0");
        require(_minAmount > 0 && _minAmount <= _amount, "Invalid min amount");
        require(_minTerm > 0 && _maxTerm >= _minTerm, "Invalid term range");
        require(_expiryDate > block.timestamp, "Expiry date must be in the future");
        
        // Generate offer hash
        bytes32 offerHash = keccak256(abi.encodePacked(_offerId, msg.sender, _amount, block.timestamp));
        
        // Ensure offer doesn't already exist
        require(loanOffers[offerHash].lender == address(0), "Offer already exists");
        
        // Create offer
        LoanOffer memory newOffer = LoanOffer({
            offerId: _offerId,
            lender: payable(msg.sender),
            amount: _amount,
            minAmount: _minAmount,
            interestRate: _interestRate,
            minTerm: _minTerm,
            maxTerm: _maxTerm,
            expiryDate: _expiryDate,
            isActive: true,
            metadataHash: _metadataHash
        });
        
        // Store offer
        loanOffers[offerHash] = newOffer;
        
        // Add offer to lender mapping
        lenderOffers[msg.sender].push(offerHash);
        
        // Emit event
        emit LoanOfferCreated(offerHash, _offerId, msg.sender, _amount, _interestRate);
        
        return offerHash;
    }

    // Function to update a loan offer
    function updateLoanOffer(
        bytes32 offerHash,
        uint256 _amount,
        uint256 _minAmount,
        uint256 _interestRate,
        uint256 _minTerm,
        uint256 _maxTerm,
        uint256 _expiryDate
    ) external onlyLender(offerHash) offerExists(offerHash) {
        // Get offer
        LoanOffer storage offer = loanOffers[offerHash];
        
        // Ensure offer is active
        require(offer.isActive, "Offer is not active");
        
        // Validate inputs
        require(_amount > 0, "Amount must be greater than 0");
        require(_minAmount > 0 && _minAmount <= _amount, "Invalid min amount");
        require(_minTerm > 0 && _maxTerm >= _minTerm, "Invalid term range");
        require(_expiryDate > block.timestamp, "Expiry date must be in the future");
        
        // Update offer
        offer.amount = _amount;
        offer.minAmount = _minAmount;
        offer.interestRate = _interestRate;
        offer.minTerm = _minTerm;
        offer.maxTerm = _maxTerm;
        offer.expiryDate = _expiryDate;
        
        // Emit event
        emit LoanOfferUpdated(offerHash, _amount, _interestRate);
    }

    // Function to cancel a loan offer
    function cancelLoanOffer(bytes32 offerHash) external onlyLender(offerHash) offerExists(offerHash) {
        // Get offer
        LoanOffer storage offer = loanOffers[offerHash];
        
        // Ensure offer is active
        require(offer.isActive, "Offer is not active");
        
        // Cancel offer
        offer.isActive = false;
        
        // Emit event
        emit LoanOfferCancelled(offerHash);
    }

    // Function to create a new loan request
    function createLoanRequest(
        string memory _requestId,
        uint256 _amount,
        uint256 _interestRate,
        uint256 _term,
        uint256 _expiryDate,
        string memory _purpose,
        string memory _metadataHash
    ) external returns (bytes32) {
        // Validate inputs
        require(_amount > 0, "Amount must be greater than 0");
        require(_term > 0, "Term must be greater than 0");
        require(_expiryDate > block.timestamp, "Expiry date must be in the future");
        
        // Generate request hash
        bytes32 requestHash = keccak256(abi.encodePacked(_requestId, msg.sender, _amount, block.timestamp));
        
        // Ensure request doesn't already exist
        require(loanRequests[requestHash].borrower == address(0), "Request already exists");
        
        // Create request
        LoanRequest memory newRequest = LoanRequest({
            requestId: _requestId,
            borrower: payable(msg.sender),
            amount: _amount,
            interestRate: _interestRate,
            term: _term,
            expiryDate: _expiryDate,
            isActive: true,
            purpose: _purpose,
            metadataHash: _metadataHash
        });
        
        // Store request
        loanRequests[requestHash] = newRequest;
        
        // Add request to borrower mapping
        borrowerRequests[msg.sender].push(requestHash);
        
        // Emit event
        emit LoanRequestCreated(requestHash, _requestId, msg.sender, _amount, _interestRate);
        
        return requestHash;
    }

    // Function to update a loan request
    function updateLoanRequest(
        bytes32 requestHash,
        uint256 _amount,
        uint256 _interestRate,
        uint256 _term,
        uint256 _expiryDate
    ) external onlyBorrower(requestHash) requestExists(requestHash) {
        // Get request
        LoanRequest storage request = loanRequests[requestHash];
        
        // Ensure request is active
        require(request.isActive, "Request is not active");
        
        // Validate inputs
        require(_amount > 0, "Amount must be greater than 0");
        require(_term > 0, "Term must be greater than 0");
        require(_expiryDate > block.timestamp, "Expiry date must be in the future");
        
        // Update request
        request.amount = _amount;
        request.interestRate = _interestRate;
        request.term = _term;
        request.expiryDate = _expiryDate;
        
        // Emit event
        emit LoanRequestUpdated(requestHash, _amount, _interestRate);
    }

    // Function to cancel a loan request
    function cancelLoanRequest(bytes32 requestHash) external onlyBorrower(requestHash) requestExists(requestHash) {
        // Get request
        LoanRequest storage request = loanRequests[requestHash];
        
        // Ensure request is active
        require(request.isActive, "Request is not active");
        
        // Cancel request
        request.isActive = false;
        
        // Emit event
        emit LoanRequestCancelled(requestHash);
    }

    // Function to match a loan offer with a loan request and create a loan agreement
    function matchLoanOfferAndRequest(
        bytes32 offerHash,
        bytes32 requestHash,
        string memory _loanId,
        uint256 _amount,
        uint256 _interestRate,
        uint256 _term,
        uint256 _startDate,
        string memory _metadataHash
    ) external onlyOwner offerExists(offerHash) requestExists(requestHash) returns (bytes32) {
        // Get offer and request
        LoanOffer storage offer = loanOffers[offerHash];
        LoanRequest storage request = loanRequests[requestHash];
        
        // Ensure offer and request are active
        require(offer.isActive, "Offer is not active");
        require(request.isActive, "Request is not active");
        
        // Ensure offer and request have not expired
        require(block.timestamp <= offer.expiryDate, "Offer has expired");
        require(block.timestamp <= request.expiryDate, "Request has expired");
        
        // Validate match parameters
        require(_amount >= offer.minAmount && _amount <= offer.amount, "Amount out of range for offer");
        require(_amount == request.amount, "Amount does not match request");
        require(_interestRate <= request.interestRate, "Interest rate too high for request");
        require(_term >= offer.minTerm && _term <= offer.maxTerm, "Term out of range for offer");
        require(_term == request.term, "Term does not match request");
        require(_startDate >= block.timestamp, "Start date must be in the future");
        
        // Create loan agreement
        bytes32 loanHash = loanAgreementContract.createLoan(
            _loanId,
            request.borrower,
            offer.lender,
            _amount,
            _interestRate,
            _term,
            _startDate,
            _metadataHash
        );
        
        // Update offer and request status
        offer.isActive = false;
        request.isActive = false;
        
        // Emit event
        emit LoanAgreementCreated(offerHash, requestHash, loanHash);
        
        return loanHash;
    }

    // Function to get loan offer details
    function getLoanOffer(bytes32 offerHash) external view offerExists(offerHash) returns (
        string memory offerId,
        address lender,
        uint256 amount,
        uint256 minAmount,
        uint256 interestRate,
        uint256 minTerm,
        uint256 maxTerm,
        uint256 expiryDate,
        bool isActive
    ) {
        LoanOffer storage offer = loanOffers[offerHash];
        
        return (
            offer.offerId,
            offer.lender,
            offer.amount,
            offer.minAmount,
            offer.interestRate,
            offer.minTerm,
            offer.maxTerm,
            offer.expiryDate,
            offer.isActive
        );
    }

    // Function to get loan request details
    function getLoanRequest(bytes32 requestHash) external view requestExists(requestHash) returns (
        string memory requestId,
        address borrower,
        uint256 amount,
        uint256 interestRate,
        uint256 term,
        uint256 expiryDate,
        bool isActive,
        string memory purpose
    ) {
        LoanRequest storage request = loanRequests[requestHash];
        
        return (
            request.requestId,
            request.borrower,
            request.amount,
            request.interestRate,
            request.term,
            request.expiryDate,
            request.isActive,
            request.purpose
        );
    }

    // Function to get offers for a lender
    function getLenderOffers(address lender) external view returns (bytes32[] memory) {
        return lenderOffers[lender];
    }

    // Function to get requests for a borrower
    function getBorrowerRequests(address borrower) external view returns (bytes32[] memory) {
        return borrowerRequests[borrower];
    }

    // Function to update platform fee (only owner)
    function updatePlatformFee(uint256 _platformFeePercent) external onlyOwner {
        platformFeePercent = _platformFeePercent;
    }

    // Function to update loan agreement contract address (only owner)
    function updateLoanAgreementContract(address _loanAgreementAddress) external onlyOwner {
        loanAgreementContract = LoanAgreement(_loanAgreementAddress);
    }
}