'use client';

import { useState } from 'react';
import Link from 'next/link';
import { LoanCard } from '@/components/loan/loan-card';
import { LoanFilter } from '@/components/loan/loan-filter';
import { Loan, LoanFilters } from '@/types/loan';

// Mock data
const mockLoans = [
  {
    id: '1',
    title: 'Working Capital Loan',
    amount: 100000,
    interest: 5.5,
    term: 12,
    company: 'Tech Startup Inc.',
    creditScore: 'A',
    purpose: 'Working capital',
    status: 'open',
    matchScore: 92,
  },
  {
    id: '2',
    title: 'Equipment Financing',
    amount: 250000,
    interest: 6.0,
    term: 24,
    company: 'Manufacturing Co.',
    creditScore: 'B+',
    purpose: 'Equipment purchase',
    status: 'open',
    matchScore: 85,
  },
  {
    id: '3',
    title: 'Expansion Funding',
    amount: 500000,
    interest: 7.2,
    term: 36,
    company: 'Retail Chain Ltd.',
    creditScore: 'A-',
    purpose: 'Business expansion',
    status: 'open',
    matchScore: 78,
  },
  {
    id: '4',
    title: 'Inventory Financing',
    amount: 75000,
    interest: 5.8,
    term: 6,
    company: 'E-commerce Store',
    creditScore: 'B',
    purpose: 'Inventory purchase',
    status: 'open',
    matchScore: 65,
  },
];

export default function Marketplace() {
  const [activeTab, setActiveTab] = useState<'borrower' | 'lender'>('borrower');
  const [filteredLoans, setFilteredLoans] = useState(mockLoans);
  
  const handleFilter = (filters: LoanFilters) => {
    // In a real app, this would call an API with the filters
    console.log('Applying filters:', filters);
    // For now, just simulate filtering by interest rate
    // if (filters.interestRate && Array.isArray(filters.interestRate)) {
    //   const [minRate, maxRate] = filters.interestRate;
    //   const filtered = mockLoans.filter(loan => 
    //     loan.interest >= minRate && 
    //     loan.interest <= maxRate
    //   );
    //   setFilteredLoans(filtered);
    // } else {
    //   setFilteredLoans(mockLoans);
    // }
  };

  return (
    <main className="container mx-auto px-4 py-8 pt-32">
      <div className="flex justify-between items-center mb-8">
        <h1 className="text-3xl font-bold">Marketplace</h1>
        <div className="flex gap-4">
          <Link 
            href="/loans/create" 
            className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
          >
            Request Loan
          </Link>
          <Link 
            href="/offers/create" 
            className="px-4 py-2 bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
          >
            Create Offer
          </Link>
        </div>
      </div>

      {/* Tabs */}
      <div className="border-b border-gray-200 mb-6">
        <div className="flex">
          <button
            className={`py-4 px-6 text-center ${
              activeTab === 'borrower'
                ? 'border-b-2 border-blue-500 text-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('borrower')}
          >
            Loan Requests
          </button>
          <button
            className={`py-4 px-6 text-center ${
              activeTab === 'lender'
                ? 'border-b-2 border-blue-500 text-blue-600'
                : 'text-gray-500 hover:text-gray-700'
            }`}
            onClick={() => setActiveTab('lender')}
          >
            Lending Offers
          </button>
        </div>
      </div>

      <div className="flex flex-col md:flex-row gap-6">
        {/* Filters */}
        <div className="w-full md:w-1/4">
          <LoanFilter onFilter={handleFilter} />
        </div>

        {/* Loan Listings */}
        <div className="w-full md:w-3/4">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-xl font-semibold">
              {activeTab === 'borrower' ? 'Available Loan Requests' : 'Available Lending Offers'}
            </h2>
            <div className="flex items-center">
              <span className="mr-2 text-sm text-gray-500">Sort by:</span>
              <select className="border rounded-md px-2 py-1 text-sm">
                <option>Match Score</option>
                <option>Interest Rate</option>
                <option>Loan Amount</option>
                <option>Term Length</option>
              </select>
            </div>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {filteredLoans.map((loan) => (
              <LoanCard key={loan.id} loan={loan} />
            ))}
          </div>
        </div>
      </div>
    </main>
  );
}