'use client';

import { motion } from 'framer-motion';

// Mock data for demonstration
const mockPortfolio = {
  totalInvested: 500000,
  activeLoans: 8,
  averageReturn: 12.5,
  totalEarnings: 45000,
  riskScore: 'Moderate',
  diversificationScore: 85,
};

const mockInvestments = [
  {
    id: '1',
    companyName: 'Tech Solutions Inc.',
    amount: 50000,
    interestRate: 15,
    term: 12,
    monthsPaid: 4,
    status: 'active',
    nextPayment: '2024-04-15',
    totalReturn: 7500,
  },
  {
    id: '2',
    companyName: 'Green Energy Co.',
    amount: 75000,
    interestRate: 12,
    term: 24,
    monthsPaid: 8,
    status: 'active',
    nextPayment: '2024-04-20',
    totalReturn: 9000,
  },
  {
    id: '3',
    companyName: 'Food Chain Ltd.',
    amount: 25000,
    interestRate: 14,
    term: 6,
    monthsPaid: 6,
    status: 'completed',
    nextPayment: null,
    totalReturn: 3500,
  },
];

export default function PortfolioPage() {
  return (
    <main className="min-h-screen pt-24 px-8">
      <div className="max-w-7xl mx-auto">
        {/* Header */}
        <div className="mb-8">
          <h1 className="text-3xl font-bold mb-2">My Portfolio</h1>
          <p className="text-gray-500">Track and manage your investments</p>
        </div>

        {/* Portfolio Overview */}
        <div className="grid grid-cols-1 md:grid-cols-3 lg:grid-cols-6 gap-6 mb-12">
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

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 }}
            className="bg-white rounded-xl p-6 shadow-sm"
          >
            <h3 className="text-gray-500 mb-2">Risk Score</h3>
            <p className="text-2xl font-bold">{mockPortfolio.riskScore}</p>
          </motion.div>

          <motion.div
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="bg-white rounded-xl p-6 shadow-sm"
          >
            <h3 className="text-gray-500 mb-2">Diversification</h3>
            <p className="text-2xl font-bold">{mockPortfolio.diversificationScore}%</p>
          </motion.div>
        </div>

        {/* Active Investments */}
        <div className="bg-white rounded-xl p-6 shadow-sm mb-8">
          <h2 className="text-xl font-semibold mb-6">Active Investments</h2>
          <div className="overflow-x-auto">
            <table className="w-full">
              <thead>
                <tr className="text-left border-b">
                  <th className="pb-4 font-medium">Company</th>
                  <th className="pb-4 font-medium">Amount</th>
                  <th className="pb-4 font-medium">Interest Rate</th>
                  <th className="pb-4 font-medium">Term</th>
                  <th className="pb-4 font-medium">Progress</th>
                  <th className="pb-4 font-medium">Status</th>
                  <th className="pb-4 font-medium">Next Payment</th>
                  <th className="pb-4 font-medium">Total Return</th>
                </tr>
              </thead>
              <tbody>
                {mockInvestments.map((investment) => (
                  <tr key={investment.id} className="border-b last:border-0">
                    <td className="py-4">{investment.companyName}</td>
                    <td className="py-4">${investment.amount.toLocaleString()}</td>
                    <td className="py-4">{investment.interestRate}%</td>
                    <td className="py-4">{investment.term} months</td>
                    <td className="py-4">
                      <div className="w-32 h-2 bg-gray-200 rounded-full">
                        <div
                          className="h-full bg-blue-600 rounded-full"
                          style={{
                            width: `${(investment.monthsPaid / investment.term) * 100}%`,
                          }}
                        />
                      </div>
                    </td>
                    <td className="py-4">
                      <span
                        className={`px-2 py-1 rounded-full text-sm ${
                          investment.status === 'active'
                            ? 'bg-green-50 text-green-700'
                            : 'bg-gray-50 text-gray-700'
                        }`}
                      >
                        {investment.status.charAt(0).toUpperCase() + investment.status.slice(1)}
                      </span>
                    </td>
                    <td className="py-4">
                      {investment.nextPayment || '-'}
                    </td>
                    <td className="py-4">${investment.totalReturn.toLocaleString()}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </main>
  );
}
