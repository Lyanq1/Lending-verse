'use client';

import { useState } from 'react';
import Link from 'next/link';
import { useParams } from 'next/navigation';

// Mock data - in a real app, this would come from an API
const mockLoan = {
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
  description: 'We are seeking working capital to expand our operations and hire additional staff. Our company has been profitable for the last 3 years with consistent growth.',
  documents: [
    { id: '1', name: 'Financial Statement 2023.pdf', type: 'financial_statement' },
    { id: '2', name: 'Business Plan.pdf', type: 'business_plan' },
    { id: '3', name: 'Cash Flow Projection.xlsx', type: 'cash_flow' },
  ],
  companyInfo: {
    name: 'Tech Startup Inc.',
    founded: 2020,
    employees: 25,
    industry: 'Software Development',
    revenue: '$1.2M (2023)',
    website: 'https://techstartup.example.com',
  }
};

export default function LoanDetails() {
  const { id } = useParams();
  const [isInterested, setIsInterested] = useState(false);
  
  // In a real app, fetch loan details based on ID
  const loan = mockLoan;
  
  return (
    <main className="container mx-auto px-4 py-8 pt-32">
      <div className="max-w-4xl mx-auto">
        {/* Breadcrumb */}
        <div className="flex items-center text-sm text-gray-500 mb-6">
          <Link href="/marketplace" className="hover:text-gray-700">
            Marketplace
          </Link>
          <span className="mx-2">/</span>
          <span className="text-gray-900">Loan #{id}</span>
        </div>
        
        {/* Loan Header */}
        <div className="flex justify-between items-center mb-6">
          <h1 className="text-3xl font-bold">{loan.title}</h1>
          <div className="flex items-center">
            <span className="text-sm font-medium text-gray-500 mr-2">Match Score:</span>
            <span className="text-lg font-bold text-green-600">{loan.matchScore}%</span>
          </div>
        </div>
        
        {/* Loan Details */}
        <div className="bg-white rounded-lg shadow overflow-hidden mb-8">
          <div className="p-6">
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
              <div>
                <h3 className="text-sm font-medium text-gray-500">Loan Amount</h3>
                <p className="text-2xl font-bold">${loan.amount.toLocaleString()}</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-500">Interest Rate</h3>
                <p className="text-2xl font-bold">{loan.interest}%</p>
              </div>
              <div>
                <h3 className="text-sm font-medium text-gray-500">Term</h3>
                <p className="text-2xl font-bold">{loan.term} months</p>
              </div>
            </div>
            
            <div className="border-t border-gray-200 pt-6">
              <h3 className="text-lg font-medium mb-4">Loan Description</h3>
              <p className="text-gray-700 mb-6">{loan.description}</p>
              
              <h3 className="text-lg font-medium mb-4">Company Information</h3>
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                <div>
                  <h4 className="text-sm font-medium text-gray-500">Company Name</h4>
                  <p className="text-gray-900">{loan.companyInfo.name}</p>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-gray-500">Founded</h4>
                  <p className="text-gray-900">{loan.companyInfo.founded}</p>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-gray-500">Employees</h4>
                  <p className="text-gray-900">{loan.companyInfo.employees}</p>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-gray-500">Industry</h4>
                  <p className="text-gray-900">{loan.companyInfo.industry}</p>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-gray-500">Annual Revenue</h4>
                  <p className="text-gray-900">{loan.companyInfo.revenue}</p>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-gray-500">Website</h4>
                  <a href={loan.companyInfo.website} target="_blank" rel="noopener noreferrer" className="text-blue-600 hover:underline">
                    {loan.companyInfo.website}
                  </a>
                </div>
              </div>
              
              <h3 className="text-lg font-medium mb-4">Credit Assessment</h3>
              <div className="flex items-center mb-6">
                <div className="w-12 h-12 rounded-full bg-green-100 flex items-center justify-center mr-4">
                  <span className="text-xl font-bold text-green-700">{loan.creditScore}</span>
                </div>
                <div>
                  <p className="text-gray-700">
                    This borrower has an excellent credit rating with a low risk of default.
                  </p>
                  <button className="text-blue-600 hover:underline text-sm mt-1">
                    Request Full Credit Report
                  </button>
                </div>
              </div>
              
              <h3 className="text-lg font-medium mb-4">Documents</h3>
              <ul className="space-y-2 mb-6">
                {loan.documents.map((doc) => (
                  <li key={doc.id} className="flex items-center p-3 bg-gray-50 rounded-md">
                    <svg className="w-5 h-5 text-gray-500 mr-3" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg">
                      <path fillRule="evenodd" d="M4 4a2 2 0 012-2h4.586A2 2 0 0112 2.586L15.414 6A2 2 0 0116 7.414V16a2 2 0 01-2 2H6a2 2 0 01-2-2V4zm2 6a1 1 0 011-1h6a1 1 0 110 2H7a1 1 0 01-1-1zm1 3a1 1 0 100 2h6a1 1 0 100-2H7z" clipRule="evenodd"></path>
                    </svg>
                    <span className="text-gray-700">{doc.name}</span>
                    <button className="ml-auto text-blue-600 hover:text-blue-800 text-sm">
                      Request Access
                    </button>
                  </li>
                ))}
              </ul>
            </div>
          </div>
          
          {/* Action Footer */}
          <div className="bg-gray-50 px-6 py-4">
            {!isInterested ? (
              <div className="flex justify-between items-center">
                <p className="text-gray-700">
                  Interested in funding this loan? Express your interest to get more details.
                </p>
                <button
                  onClick={() => setIsInterested(true)}
                  className="px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700"
                >
                  I&apos;m Interested
                </button>
              </div>
            ) : (
              <div className="flex justify-between items-center">
                <p className="text-green-700 font-medium">
                  Thank you for your interest! A representative will contact you shortly.
                </p>
                <button
                  className="px-4 py-2 bg-green-600 text-white rounded-md hover:bg-green-700"
                >
                  Make Offer
                </button>
              </div>
            )}
          </div>
        </div>
        
        {/* Similar Loans */}
        <div>
          <h2 className="text-xl font-semibold mb-4">Similar Loan Requests</h2>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-white rounded-lg shadow p-4 border border-gray-200">
              <div className="flex justify-between">
                <h3 className="font-medium">Equipment Financing</h3>
                <span className="text-sm text-blue-600">85% match</span>
              </div>
              <p className="text-sm text-gray-500 mb-2">Manufacturing Co.</p>
              <div className="flex justify-between text-sm">
                <span>$250,000</span>
                <span>6.0% interest</span>
                <span>24 months</span>
              </div>
            </div>
            <div className="bg-white rounded-lg shadow p-4 border border-gray-200">
              <div className="flex justify-between">
                <h3 className="font-medium">Expansion Funding</h3>
                <span className="text-sm text-blue-600">78% match</span>
              </div>
              <p className="text-sm text-gray-500 mb-2">Retail Chain Ltd.</p>
              <div className="flex justify-between text-sm">
                <span>$500,000</span>
                <span>7.2% interest</span>
                <span>36 months</span>
              </div>
            </div>
          </div>
        </div>
      </div>
    </main>
  );
}