'use client';

import Link from 'next/link';

interface LoanCardProps {
  loan: {
    id: string;
    title: string;
    amount: number;
    interest: number;
    term: number;
    company: string;
    creditScore: string;
    purpose: string;
    status: string;
    matchScore: number;
  };
}

export function LoanCard({ loan }: LoanCardProps) {
  return (
    <div className="bg-white rounded-lg shadow overflow-hidden border border-gray-200 hover:shadow-md transition-shadow">
      <div className="p-5">
        <div className="flex justify-between items-start">
          <h3 className="text-lg font-semibold text-gray-900 mb-1">{loan.title}</h3>
          <div className="flex items-center">
            <span className="text-sm font-medium text-gray-500 mr-1">Match:</span>
            <span className={`text-sm font-bold ${
              loan.matchScore >= 90 ? 'text-green-600' : 
              loan.matchScore >= 70 ? 'text-blue-600' : 'text-orange-600'
            }`}>
              {loan.matchScore}%
            </span>
          </div>
        </div>
        
        <p className="text-sm text-gray-500 mb-4">{loan.company}</p>
        
        <div className="grid grid-cols-2 gap-4 mb-4">
          <div>
            <p className="text-xs text-gray-500">Amount</p>
            <p className="text-base font-medium">${loan.amount.toLocaleString()}</p>
          </div>
          <div>
            <p className="text-xs text-gray-500">Interest Rate</p>
            <p className="text-base font-medium">{loan.interest}%</p>
          </div>
          <div>
            <p className="text-xs text-gray-500">Term</p>
            <p className="text-base font-medium">{loan.term} months</p>
          </div>
          <div>
            <p className="text-xs text-gray-500">Credit Score</p>
            <p className="text-base font-medium">{loan.creditScore}</p>
          </div>
        </div>
        
        <div className="flex items-center justify-between mt-4 pt-4 border-t border-gray-100">
          <div>
            <span className={`px-2 py-1 text-xs font-semibold rounded-full 
              ${loan.status === 'open' ? 'bg-green-100 text-green-800' : 
                loan.status === 'pending' ? 'bg-yellow-100 text-yellow-800' : 
                'bg-gray-100 text-gray-800'}`}>
              {loan.status}
            </span>
          </div>
          <Link 
            href={`/loans/${loan.id}`}
            className="text-blue-600 hover:text-blue-800 text-sm font-medium"
          >
            View Details
          </Link>
        </div>
      </div>
    </div>
  );
}