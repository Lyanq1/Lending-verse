'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';

// Mock data for demonstration
const mockLoanOpportunities = [
  {
    id: '1',
    companyName: 'Tech Solutions Inc.',
    amount: 100000,
    term: 12,
    interestRate: 15,
    creditScore: 'A',
    purpose: 'Expansion',
    matchScore: 92,
    industry: 'Technology',
    location: 'Ho Chi Minh City',
  },
  {
    id: '2',
    companyName: 'Green Energy Co.',
    amount: 250000,
    term: 24,
    interestRate: 12,
    creditScore: 'A-',
    purpose: 'Equipment',
    matchScore: 88,
    industry: 'Energy',
    location: 'Ha Noi',
  },
  {
    id: '3',
    companyName: 'Food Chain Ltd.',
    amount: 75000,
    term: 6,
    interestRate: 14,
    creditScore: 'B+',
    purpose: 'Working Capital',
    matchScore: 85,
    industry: 'Food & Beverage',
    location: 'Da Nang',
  },
];

export default function LoanOpportunitiesPage() {
  const [sortBy, setSortBy] = useState('matchScore');

  return (
    <main className="min-h-screen pt-24 px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="flex justify-between items-center mb-8">
          <div>
            <h1 className="text-3xl font-bold mb-2">Loan Opportunities</h1>
            <p className="text-gray-500">Find the best matches for your investment portfolio</p>
          </div>
          
          {/* Sort Options */}
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            className="px-4 py-2 border rounded-lg bg-white"
          >
            <option value="matchScore">Match Score</option>
            <option value="amount">Loan Amount</option>
            <option value="interestRate">Interest Rate</option>
            <option value="term">Term Length</option>
          </select>
        </div>

        {/* Filters */}
        <div className="bg-white rounded-lg p-6 mb-8 shadow-sm">
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
            <input
              type="text"
              placeholder="Search by company name"
              className="px-4 py-2 border rounded-lg"
            />
            <select className="px-4 py-2 border rounded-lg">
              <option value="">All Industries</option>
              <option value="technology">Technology</option>
              <option value="energy">Energy</option>
              <option value="food">Food & Beverage</option>
            </select>
            <select className="px-4 py-2 border rounded-lg">
              <option value="">All Locations</option>
              <option value="hcm">Ho Chi Minh City</option>
              <option value="hanoi">Ha Noi</option>
              <option value="danang">Da Nang</option>
            </select>
            <button className="px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700">
              Apply Filters
            </button>
          </div>
        </div>

        {/* Loan Cards */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {mockLoanOpportunities.map((loan) => (
            <motion.div
              key={loan.id}
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              className="bg-white rounded-xl p-6 shadow-sm border border-gray-100"
            >
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h3 className="font-semibold text-lg">{loan.companyName}</h3>
                  <div className="flex items-center text-sm text-gray-500 mt-1">
                    <span>{loan.industry}</span>
                    <span className="mx-2">•</span>
                    <span>{loan.location}</span>
                  </div>
                </div>
                <div className="bg-green-50 text-green-700 px-3 py-1 rounded-full text-sm font-medium">
                  {loan.matchScore}% Match
                </div>
              </div>

              <div className="space-y-3">
                <div className="flex justify-between">
                  <span className="text-gray-500">Amount</span>
                  <span className="font-medium">${loan.amount.toLocaleString()}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Term</span>
                  <span className="font-medium">{loan.term} months</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Interest Rate</span>
                  <span className="font-medium">{loan.interestRate}%</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Credit Score</span>
                  <span className="font-medium">{loan.creditScore}</span>
                </div>
                <div className="flex justify-between">
                  <span className="text-gray-500">Purpose</span>
                  <span className="font-medium">{loan.purpose}</span>
                </div>
              </div>

              <div className="mt-6 flex space-x-3">
                <button className="flex-1 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors">
                  Invest Now
                </button>
                <button className="flex-1 border border-gray-200 py-2 px-4 rounded-lg hover:bg-gray-50 transition-colors">
                  View Details
                </button>
              </div>
            </motion.div>
          ))}
        </div>
      </div>
    </main>
  );
}
