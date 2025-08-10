export interface LoanFilters {
  amount?: [number, number];
  interestRate?: [number, number];
  term?: [number, number];
  creditScore?: string[];
  purpose?: string[];
}

export interface Loan {
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
}
