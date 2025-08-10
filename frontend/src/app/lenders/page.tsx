'use client';

import { useState } from 'react';
import { motion } from 'framer-motion';

// Mock data for demonstration
const mockPortfolio = {
  totalInvested: 500000,
  activeLoans: 8,
  averageReturn: 12.5,
  totalEarnings: 45000,
};

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
  },
];

export default function LendersPage() {
  const [activeTab, setActiveTab] = useState('opportunities');

  return (
    <main className="min-h-screen pt-24 px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header Section */}
        <div className="mb-12">
          <h1 className="text-4xl font-bold mb-4">Lender Dashboard</h1>
          <p className="text-gray-500">
            Find high-quality borrowers and manage your lending portfolio
          </p>
        </div>

        {/* Portfolio Overview */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            className="bg-white rounded-xl p-6 shadow-sm"
          >
            <h3 className="text-gray-500 mb-2">Total Invested</h3>
            <p className="text-2xl font-bold">${mockPortfolio.totalInvested.toLocaleString()}</p>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.1 }}
            className="bg-white rounded-xl p-6 shadow-sm"
          >
            <h3 className="text-gray-500 mb-2">Active Loans</h3>
            <p className="text-2xl font-bold">{mockPortfolio.activeLoans}</p>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 }}
            className="bg-white rounded-xl p-6 shadow-sm"
          >
            <h3 className="text-gray-500 mb-2">Average Return</h3>
            <p className="text-2xl font-bold">{mockPortfolio.averageReturn}%</p>
          </motion.div>
          
          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="bg-white rounded-xl p-6 shadow-sm"
          >
            <h3 className="text-gray-500 mb-2">Total Earnings</h3>
            <p className="text-2xl font-bold">${mockPortfolio.totalEarnings.toLocaleString()}</p>
          </motion.div>
        </div>

        {/* Tabs */}
        <div className="border-b border-gray-200 mb-8">
          <nav className="flex space-x-8">
            <button
              onClick={() => setActiveTab('opportunities')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'opportunities'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Loan Opportunities
            </button>
            <button
              onClick={() => setActiveTab('portfolio')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'portfolio'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              My Portfolio
            </button>
            <button
              onClick={() => setActiveTab('analytics')}
              className={`py-4 px-1 border-b-2 font-medium text-sm ${
                activeTab === 'analytics'
                  ? 'border-blue-500 text-blue-600'
                  : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
              }`}
            >
              Analytics
            </button>
          </nav>
        </div>

        {/* Loan Opportunities */}
        {activeTab === 'opportunities' && (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {mockLoanOpportunities.map((loan) => (
              <motion.div
                key={loan.id}
                initial={{ opacity: 0, scale: 0.95 }}
                animate={{ opacity: 1, scale: 1 }}
                className="bg-white rounded-xl p-6 shadow-sm border border-gray-100"
              >
                <div className="flex justify-between items-start mb-4">
                  <div>
                    <h3 className="font-semibold text-lg">{loan.companyName}</h3>
                    <p className="text-gray-500 text-sm">{loan.purpose}</p>
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
                </div>

                <button className="w-full mt-6 bg-blue-600 text-white py-2 px-4 rounded-lg hover:bg-blue-700 transition-colors">
                  View Details
                </button>
              </motion.div>
            ))}
          </div>
        )}

        {/* Portfolio Tab */}
        {activeTab === 'portfolio' && (
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Active Investments</h2>
            <p className="text-gray-500">Portfolio management coming soon...</p>
          </div>
        )}

        {/* Analytics Tab */}
        {activeTab === 'analytics' && (
          <div className="bg-white rounded-xl p-6 shadow-sm">
            <h2 className="text-xl font-semibold mb-4">Investment Analytics</h2>
            <p className="text-gray-500">Analytics dashboard coming soon...</p>
          </div>
        )}
      </div>
    </main>
  );
}
