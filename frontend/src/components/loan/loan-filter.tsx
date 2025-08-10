'use client';

import { useState } from 'react';
import { LoanFilters } from '@/types/loan';

interface LoanFilterProps {
  onFilter: (filters: LoanFilters) => void;
}

export function LoanFilter({ onFilter }: LoanFilterProps) {
  const [filters, setFilters] = useState({
    amount: [0, 1000000],
    interestRate: [0, 15],
    term: [0, 60],
    creditScore: [] as string[],
    purpose: [] as string[],
  });

  const handleRangeChange = (name: string, value: [number, number]) => {
    setFilters(prev => ({ ...prev, [name]: value }));
  };

  const handleCheckboxChange = (name: string, value: string, checked: boolean) => {
    setFilters(prev => {
      const currentValues = prev[name as keyof typeof prev] as string[];
      if (checked) {
        return { ...prev, [name]: [...currentValues, value] };
      } else {
        return { ...prev, [name]: currentValues.filter(v => v !== value) };
      }
    });
  };

  const handleApplyFilters = () => {
    // onFilter(filters);
  };

  const handleResetFilters = () => {
    setFilters({
      amount: [0, 1000000],
      interestRate: [0, 15],
      term: [0, 60],
      creditScore: [],
      purpose: [],
    });
    onFilter({});
  };

  return (
    <div className="bg-white rounded-lg shadow p-5">
      <h3 className="text-lg font-semibold mb-4">Filters</h3>
      
      {/* Amount Range */}
      <div className="mb-5">
        <h4 className="text-sm font-medium mb-2">Loan Amount</h4>
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500">${filters.amount[0].toLocaleString()}</span>
          <span className="text-xs text-gray-500">${filters.amount[1].toLocaleString()}</span>
        </div>
        <input
          type="range"
          min="0"
          max="1000000"
          value={filters.amount[1]}
          onChange={(e) => handleRangeChange('amount', [filters.amount[0], parseInt(e.target.value)])}
          className="w-full mt-1"
        />
      </div>
      
      {/* Interest Rate Range */}
      <div className="mb-5">
        <h4 className="text-sm font-medium mb-2">Interest Rate (%)</h4>
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500">{filters.interestRate[0]}%</span>
          <span className="text-xs text-gray-500">{filters.interestRate[1]}%</span>
        </div>
        <input
          type="range"
          min="0"
          max="15"
          step="0.5"
          value={filters.interestRate[1]}
          onChange={(e) => handleRangeChange('interestRate', [filters.interestRate[0], parseFloat(e.target.value)])}
          className="w-full mt-1"
        />
      </div>
      
      {/* Term Range */}
      <div className="mb-5">
        <h4 className="text-sm font-medium mb-2">Term (months)</h4>
        <div className="flex items-center justify-between">
          <span className="text-xs text-gray-500">{filters.term[0]} months</span>
          <span className="text-xs text-gray-500">{filters.term[1]} months</span>
        </div>
        <input
          type="range"
          min="0"
          max="60"
          step="6"
          value={filters.term[1]}
          onChange={(e) => handleRangeChange('term', [filters.term[0], parseInt(e.target.value)])}
          className="w-full mt-1"
        />
      </div>
      
      {/* Credit Score */}
      <div className="mb-5">
        <h4 className="text-sm font-medium mb-2">Credit Score</h4>
        <div className="space-y-2">
          {['A', 'B', 'C', 'D'].map((score) => (
            <div key={score} className="flex items-center">
              <input
                type="checkbox"
                id={`credit-${score}`}
                checked={filters.creditScore.includes(score)}
                onChange={(e) => handleCheckboxChange('creditScore', score, e.target.checked)}
                className="mr-2"
              />
              <label htmlFor={`credit-${score}`} className="text-sm text-gray-700">
                {score}
              </label>
            </div>
          ))}
        </div>
      </div>
      
      {/* Loan Purpose */}
      <div className="mb-5">
        <h4 className="text-sm font-medium mb-2">Loan Purpose</h4>
        <div className="space-y-2">
          {[
            { id: 'working_capital', label: 'Working Capital' },
            { id: 'equipment', label: 'Equipment Purchase' },
            { id: 'expansion', label: 'Business Expansion' },
            { id: 'inventory', label: 'Inventory' },
            { id: 'refinancing', label: 'Debt Refinancing' },
          ].map((purpose) => (
            <div key={purpose.id} className="flex items-center">
              <input
                type="checkbox"
                id={`purpose-${purpose.id}`}
                checked={filters.purpose.includes(purpose.id)}
                onChange={(e) => handleCheckboxChange('purpose', purpose.id, e.target.checked)}
                className="mr-2"
              />
              <label htmlFor={`purpose-${purpose.id}`} className="text-sm text-gray-700">
                {purpose.label}
              </label>
            </div>
          ))}
        </div>
      </div>
      
      {/* Action Buttons */}
      <div className="flex space-x-3">
        <button
          onClick={handleApplyFilters}
          className="flex-1 px-4 py-2 bg-blue-600 text-white rounded-md hover:bg-blue-700 text-sm"
        >
          Apply Filters
        </button>
        <button
          onClick={handleResetFilters}
          className="px-4 py-2 text-gray-700 bg-gray-200 rounded-md hover:bg-gray-300 text-sm"
        >
          Reset
        </button>
      </div>
    </div>
  );
}