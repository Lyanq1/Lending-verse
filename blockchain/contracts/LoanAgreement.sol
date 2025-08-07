// SPDX-License-Identifier: MIT
pragma solidity ^0.8.17;

/**
 * @title LoanAgreement
 * @dev Smart contract for P2P lending agreements between lenders and borrowers
 */
contract LoanAgreement {
    // Loan status enum
    enum LoanStatus {
        Pending,    // Loan agreement created but not funded
        Active,     // Loan is funded and active
        Completed,  // Loan fully repaid
        Defaulted,  // Loan defaulted
        Cancelled   // Loan cancelled before funding
    }

    // Payment status enum
    enum PaymentStatus {
        Pending,    // Payment is due but not paid
        Paid,       // Payment is completed
        Late,       // Payment is late
        Defaulted   // Payment defaulted
    }

    // Payment struct
    struct Payment {
        uint256 amount;        // Payment amount
        uint256 dueDate;       // Due date timestamp
        uint256 paidDate;      // Paid date timestamp (0 if not paid)
        PaymentStatus status;  // Payment status
    }

    // Loan struct
    struct Loan {
        string loanId;                // Unique loan ID from backend
        address payable borrower;     // Borrower address
        address payable lender;       // Lender address
        uint256 principal;            // Loan principal amount
        uint256 interestRate;         // Annual interest rate (in basis points, e.g., 500 = 5%)
        uint256 term;                 // Loan term in months
        uint256 startDate;            // Loan start date timestamp
        uint256 endDate;              // Loan end date timestamp
        uint256 nextPaymentIndex;     // Index of the next payment due
        LoanStatus status;            // Loan status
        uint256 totalRepaid;          // Total amount repaid so far
        string metadataHash;          // IPFS hash for additional loan metadata
    }

    // State variables
    mapping(bytes32 => Loan) public loans;
    mapping(bytes32 => Payment[]) public payments;
    mapping(address => bytes32[]) public borrowerLoans;
    mapping(address => bytes32[]) public lenderLoans;
    
    address public owner;
    uint256 public platformFeePercent; // Platform fee in basis points (e.g., 100 = 1%)

    // Events
    event LoanCreated(bytes32 indexed loanHash, string loanId, address borrower, address lender, uint256 principal);
    event LoanFunded(bytes32 indexed loanHash, uint256 amount);
    event PaymentMade(bytes32 indexed loanHash, uint256 paymentIndex, uint256 amount);
    event LoanCompleted(bytes32 indexed loanHash);
    event LoanDefaulted(bytes32 indexed loanHash);
    event LoanCancelled(bytes32 indexed loanHash);

    // Constructor
    constructor(uint256 _platformFeePercent) {
        owner = msg.sender;
        platformFeePercent = _platformFeePercent;
    }

    // Modifiers
    modifier onlyOwner() {
        require(msg.sender == owner, "Only owner can call this function");
        _;
    }

    modifier onlyBorrower(bytes32 loanHash) {
        require(msg.sender == loans[loanHash].borrower, "Only borrower can call this function");
        _;
    }

    modifier onlyLender(bytes32 loanHash) {
        require(msg.sender == loans[loanHash].lender, "Only lender can call this function");
        _;
    }

    modifier loanExists(bytes32 loanHash) {
        require(loans[loanHash].borrower != address(0), "Loan does not exist");
        _;
    }

    // Function to create a new loan agreement
    function createLoan(
        string memory _loanId,
        address payable _borrower,
        address payable _lender,
        uint256 _principal,
        uint256 _interestRate,
        uint256 _term,
        uint256 _startDate,
        string memory _metadataHash
    ) external returns (bytes32) {
        // Generate loan hash
        bytes32 loanHash = keccak256(abi.encodePacked(_loanId, _borrower, _lender, _principal, block.timestamp));
        
        // Ensure loan doesn't already exist
        require(loans[loanHash].borrower == address(0), "Loan already exists");
        
        // Calculate end date
        uint256 _endDate = _startDate + (_term * 30 days);
        
        // Create loan
        Loan memory newLoan = Loan({
            loanId: _loanId,
            borrower: _borrower,
            lender: _lender,
            principal: _principal,
            interestRate: _interestRate,
            term: _term,
            startDate: _startDate,
            endDate: _endDate,
            nextPaymentIndex: 0,
            status: LoanStatus.Pending,
            totalRepaid: 0,
            metadataHash: _metadataHash
        });
        
        // Store loan
        loans[loanHash] = newLoan;
        
        // Add loan to borrower and lender mappings
        borrowerLoans[_borrower].push(loanHash);
        lenderLoans[_lender].push(loanHash);
        
        // Create payment schedule
        _createPaymentSchedule(loanHash, _principal, _interestRate, _term, _startDate);
        
        // Emit event
        emit LoanCreated(loanHash, _loanId, _borrower, _lender, _principal);
        
        return loanHash;
    }

    // Function to fund a loan
    function fundLoan(bytes32 loanHash) external payable onlyLender(loanHash) loanExists(loanHash) {
        Loan storage loan = loans[loanHash];
        
        // Ensure loan is in pending status
        require(loan.status == LoanStatus.Pending, "Loan is not in pending status");
        
        // Ensure correct amount is sent
        require(msg.value == loan.principal, "Incorrect funding amount");
        
        // Update loan status
        loan.status = LoanStatus.Active;
        
        // Transfer funds to borrower
        uint256 platformFee = (loan.principal * platformFeePercent) / 10000;
        uint256 borrowerAmount = loan.principal - platformFee;
        
        // Transfer platform fee
        payable(owner).transfer(platformFee);
        
        // Transfer principal to borrower
        loan.borrower.transfer(borrowerAmount);
        
        // Emit event
        emit LoanFunded(loanHash, loan.principal);
    }

    // Function to make a loan payment
    function makePayment(bytes32 loanHash) external payable onlyBorrower(loanHash) loanExists(loanHash) {
        Loan storage loan = loans[loanHash];
        
        // Ensure loan is active
        require(loan.status == LoanStatus.Active, "Loan is not active");
        
        // Ensure there are payments remaining
        require(loan.nextPaymentIndex < payments[loanHash].length, "No payments remaining");
        
        // Get next payment
        Payment storage payment = payments[loanHash][loan.nextPaymentIndex];
        
        // Ensure correct amount is sent
        require(msg.value == payment.amount, "Incorrect payment amount");
        
        // Update payment
        payment.paidDate = block.timestamp;
        payment.status = PaymentStatus.Paid;
        
        // Update loan
        loan.totalRepaid += payment.amount;
        loan.nextPaymentIndex++;
        
        // Check if loan is fully repaid
        if (loan.nextPaymentIndex == payments[loanHash].length) {
            loan.status = LoanStatus.Completed;
            emit LoanCompleted(loanHash);
        }
        
        // Transfer payment to lender
        loan.lender.transfer(msg.value);
        
        // Emit event
        emit PaymentMade(loanHash, loan.nextPaymentIndex - 1, payment.amount);
    }

    // Function to mark a loan as defaulted (can only be called by contract owner or lender)
    function markAsDefaulted(bytes32 loanHash) external loanExists(loanHash) {
        require(msg.sender == owner || msg.sender == loans[loanHash].lender, "Unauthorized");
        
        Loan storage loan = loans[loanHash];
        
        // Ensure loan is active
        require(loan.status == LoanStatus.Active, "Loan is not active");
        
        // Ensure there are payments remaining
        require(loan.nextPaymentIndex < payments[loanHash].length, "No payments remaining");
        
        // Get next payment
        Payment storage payment = payments[loanHash][loan.nextPaymentIndex];
        
        // Ensure payment is late
        require(block.timestamp > payment.dueDate + 30 days, "Payment is not late enough to default");
        
        // Mark payment as defaulted
        payment.status = PaymentStatus.Defaulted;
        
        // Mark loan as defaulted
        loan.status = LoanStatus.Defaulted;
        
        // Emit event
        emit LoanDefaulted(loanHash);
    }

    // Function to cancel a loan (can only be called before funding)
    function cancelLoan(bytes32 loanHash) external loanExists(loanHash) {
        Loan storage loan = loans[loanHash];
        
        // Ensure loan is pending
        require(loan.status == LoanStatus.Pending, "Loan is not in pending status");
        
        // Ensure caller is borrower, lender, or owner
        require(
            msg.sender == loan.borrower || 
            msg.sender == loan.lender || 
            msg.sender == owner, 
            "Unauthorized"
        );
        
        // Mark loan as cancelled
        loan.status = LoanStatus.Cancelled;
        
        // Emit event
        emit LoanCancelled(loanHash);
    }

    // Function to get loan details
    function getLoan(bytes32 loanHash) external view loanExists(loanHash) returns (
        string memory loanId,
        address borrower,
        address lender,
        uint256 principal,
        uint256 interestRate,
        uint256 term,
        uint256 startDate,
        uint256 endDate,
        uint256 nextPaymentIndex,
        LoanStatus status,
        uint256 totalRepaid
    ) {
        Loan storage loan = loans[loanHash];
        
        return (
            loan.loanId,
            loan.borrower,
            loan.lender,
            loan.principal,
            loan.interestRate,
            loan.term,
            loan.startDate,
            loan.endDate,
            loan.nextPaymentIndex,
            loan.status,
            loan.totalRepaid
        );
    }

    // Function to get payment details
    function getPayment(bytes32 loanHash, uint256 paymentIndex) external view loanExists(loanHash) returns (
        uint256 amount,
        uint256 dueDate,
        uint256 paidDate,
        PaymentStatus status
    ) {
        require(paymentIndex < payments[loanHash].length, "Payment index out of bounds");
        
        Payment storage payment = payments[loanHash][paymentIndex];
        
        return (
            payment.amount,
            payment.dueDate,
            payment.paidDate,
            payment.status
        );
    }

    // Function to get number of payments for a loan
    function getPaymentCount(bytes32 loanHash) external view loanExists(loanHash) returns (uint256) {
        return payments[loanHash].length;
    }

    // Function to get loans for a borrower
    function getBorrowerLoans(address borrower) external view returns (bytes32[] memory) {
        return borrowerLoans[borrower];
    }

    // Function to get loans for a lender
    function getLenderLoans(address lender) external view returns (bytes32[] memory) {
        return lenderLoans[lender];
    }

    // Function to update platform fee (only owner)
    function updatePlatformFee(uint256 _platformFeePercent) external onlyOwner {
        platformFeePercent = _platformFeePercent;
    }

    // Internal function to create payment schedule
    function _createPaymentSchedule(
        bytes32 loanHash,
        uint256 _principal,
        uint256 _interestRate,
        uint256 _term,
        uint256 _startDate
    ) internal {
        // Calculate monthly payment (simplified)
        uint256 monthlyInterestRate = _interestRate / 12 / 10000; // Convert basis points to decimal and divide by 12
        uint256 monthlyPayment = (_principal * (monthlyInterestRate * (1 + monthlyInterestRate) ** _term)) / 
                                ((1 + monthlyInterestRate) ** _term - 1);
        
        // Create payment schedule
        for (uint256 i = 0; i < _term; i++) {
            uint256 dueDate = _startDate + ((i + 1) * 30 days);
            
            Payment memory newPayment = Payment({
                amount: monthlyPayment,
                dueDate: dueDate,
                paidDate: 0,
                status: PaymentStatus.Pending
            });
            
            payments[loanHash].push(newPayment);
        }
        
        // Adjust last payment to account for rounding errors
        uint256 totalPayments = monthlyPayment * _term;
        if (totalPayments != _principal) {
            uint256 lastIndex = _term - 1;
            payments[loanHash][lastIndex].amount += (totalPayments - _principal);
        }
    }
}