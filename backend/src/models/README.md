# Database Schema for LendingVerse P2P Lending Platform

This document describes the database schema for the LendingVerse P2P lending platform, which connects businesses seeking loans with lenders.

## Core Entities

### User System

- **User**: Base model for all users with authentication details
- **Profile**: Personal information for users
- **Business**: Company information for businesses
- **LenderProfile**: Additional information for users who are lenders
- **BorrowerProfile**: Additional information for users who are borrowers

### Loan System

- **LoanRequest**: Loan requests from borrowers
- **LoanOffer**: Offers from lenders
- **LoanMatch**: Matches between loan requests and offers
- **LoanAgreement**: Finalized loan agreements
- **Payment**: Loan repayments

### Supporting Entities

- **Document**: Files uploaded by users
- **CreditReport**: Credit assessment for borrowers
- **RefreshToken**: For authentication
- **Notification**: System notifications
- **Activity**: User activity logs

## Entity Relationships

### User Relationships

```
User
├── Profile (1:1)
├── Business (1:1)
├── LenderProfile (1:1, optional)
├── BorrowerProfile (1:1, optional)
├── RefreshTokens (1:N)
├── Notifications (1:N)
└── Activities (1:N)
```

### Loan Relationships

```
Business
├── LoanRequests (1:N)
└── LoanOffers (1:N)

LoanRequest
├── Documents (1:N)
├── Matches (1:N)
└── LoanAgreement (1:1, optional)

LoanOffer
└── Matches (1:N)

LoanMatch
└── LoanAgreement (1:1, optional)

LoanAgreement
├── Payments (1:N)
└── Documents (1:N)
```

## Key Features of the Schema

### User & Business Management

- Support for both individual and business users
- Separate profiles for lenders and borrowers
- Detailed business information storage

### Loan Lifecycle

1. **Creation**: Borrowers create LoanRequests, Lenders create LoanOffers
2. **Matching**: System creates LoanMatches between compatible requests and offers
3. **Agreement**: When a match is accepted, a LoanAgreement is created
4. **Repayment**: Payments are tracked against the LoanAgreement

### Document Management

- Support for various document types (financial statements, business plans, etc.)
- Document verification tracking
- Association with businesses, loan requests, and agreements

### Credit Assessment

- Storage of credit scores and reports
- Risk level classification
- Historical credit data

### Security & Authentication

- Password hashing
- Refresh token system
- Activity logging

## Enums

- **LoanStatus**: DRAFT, PENDING, ACTIVE, FUNDED, REJECTED, EXPIRED, COMPLETED
- **OfferStatus**: DRAFT, ACTIVE, MATCHED, EXPIRED, WITHDRAWN
- **MatchStatus**: PENDING, ACCEPTED, REJECTED, EXPIRED
- **AgreementStatus**: PENDING, ACTIVE, COMPLETED, DEFAULTED, CANCELLED
- **PaymentStatus**: PENDING, PAID, LATE, DEFAULTED
- **PaymentFrequency**: WEEKLY, BIWEEKLY, MONTHLY, QUARTERLY
- **DocumentType**: FINANCIAL_STATEMENT, BUSINESS_PLAN, TAX_RETURN, BANK_STATEMENT, IDENTITY_VERIFICATION, BUSINESS_REGISTRATION, LOAN_AGREEMENT, OTHER
- **RiskLevel**: VERY_LOW, LOW, MEDIUM, HIGH, VERY_HIGH

## Blockchain Integration

The schema includes fields for blockchain integration:
- `contractHash` in LoanAgreement for storing the hash of the smart contract
- `transactionHash` in Payment for tracking blockchain transactions
- `fileHash` in Document for document verification on the blockchain

## Notes on Implementation

- The schema is designed for use with Prisma ORM
- PostgreSQL is the recommended database provider
- Timestamps (createdAt, updatedAt) are included on all relevant models for auditing
- Unique constraints and relationships are defined to maintain data integrity