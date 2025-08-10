'use client';

import Link from "next/link";
import Image from "next/image";
import { useState } from "react";

export function Navbar() {
  const [isLenderMenuOpen, setIsLenderMenuOpen] = useState(false);
  const [isBorrowerMenuOpen, setIsBorrowerMenuOpen] = useState(false);

  return (
    <nav className="fixed top-0 left-0 right-0 z-50 bg-white/80 backdrop-blur-sm border-b">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center justify-between h-16">
          {/* Logo and Brand Name */}
          <div className="flex items-center">
            <Link href="/" className="flex items-center space-x-2">
              <Image src="/logo.png" alt="LendingVerse Logo" width={180} height={32} />
            </Link>
          </div>

          {/* Navigation Links */}
          <div className="hidden md:flex items-center space-x-8">
            <Link href="/marketplace" className="text-gray-600 hover:text-gray-900">
              Marketplace
            </Link>
            <Link href="/dashboard" className="text-gray-600 hover:text-gray-900">
              Dashboard
            </Link>
            
            {/* Lender Dropdown */}
            <div className="relative">
              <button
                className="text-gray-600 hover:text-gray-900 flex items-center space-x-1"
                onMouseEnter={() => setIsLenderMenuOpen(true)}
                onMouseLeave={() => setIsLenderMenuOpen(false)}
              >
                <span>For Lenders</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              
              {isLenderMenuOpen && (
                <div
                  className="absolute top-full left-0 w-48 py-2 mt-1 bg-white rounded-lg shadow-lg border"
                  onMouseEnter={() => setIsLenderMenuOpen(true)}
                  onMouseLeave={() => setIsLenderMenuOpen(false)}
                >
                  <Link
                    href="/lenders"
                    className="block px-4 py-2 text-gray-600 hover:bg-gray-50"
                  >
                    Lender Dashboard
                  </Link>
                  <Link
                    href="/lenders/opportunities"
                    className="block px-4 py-2 text-gray-600 hover:bg-gray-50"
                  >
                    Loan Opportunities
                  </Link>
                  <Link
                    href="/lenders/portfolio"
                    className="block px-4 py-2 text-gray-600 hover:bg-gray-50"
                  >
                    My Portfolio
                  </Link>
                </div>
              )}
            </div>

            {/* Borrower Dropdown */}
            <div className="relative">
              <button
                className="text-gray-600 hover:text-gray-900 flex items-center space-x-1"
                onMouseEnter={() => setIsBorrowerMenuOpen(true)}
                onMouseLeave={() => setIsBorrowerMenuOpen(false)}
              >
                <span>For Borrowers</span>
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 9l-7 7-7-7" />
                </svg>
              </button>
              
              {isBorrowerMenuOpen && (
                <div
                  className="absolute top-full left-0 w-48 py-2 mt-1 bg-white rounded-lg shadow-lg border"
                  onMouseEnter={() => setIsBorrowerMenuOpen(true)}
                  onMouseLeave={() => setIsBorrowerMenuOpen(false)}
                >
                  <Link
                    href="/loans/create"
                    className="block px-4 py-2 text-gray-600 hover:bg-gray-50"
                  >
                    Apply for Loan
                  </Link>
                  <Link
                    href="/loans/my-loans"
                    className="block px-4 py-2 text-gray-600 hover:bg-gray-50"
                  >
                    My Loans
                  </Link>
                  <Link
                    href="/loans/calculator"
                    className="block px-4 py-2 text-gray-600 hover:bg-gray-50"
                  >
                    Loan Calculator
                  </Link>
                </div>
              )}
            </div>
          </div>

          {/* Auth Buttons */}
          <div className="flex items-center space-x-4">
            <Link 
              href="/login"
              className="text-gray-600 hover:text-gray-900"
            >
              Log in
            </Link>
            <Link
              href="/register"
              className="px-4 py-2 rounded-lg bg-blue-600 text-white hover:bg-blue-700 transition-colors"
            >
              Register
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
}