'use client';

import { useEffect, useRef, useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { TransactionAnimation } from './transaction-animation';

interface Partner {
  id: string;
  name: string;
  logo: string;
  type: 'business' | 'individual';
  status?: 'active' | 'requesting' | 'matching';
  requestAmount?: number;
}

interface Transaction {
  id: string;
  from: string;
  to: string;
  amount: number;
  status: 'pending' | 'matching' | 'completed';
}

interface TransactionCircleProps {
  partners: Partner[];
}

export function TransactionCircle({ partners }: TransactionCircleProps) {
  const containerRef = useRef<HTMLDivElement>(null);
  const [activeTransactions, setActiveTransactions] = useState<Transaction[]>([]);
  const [hoveredPartner, setHoveredPartner] = useState<Partner | null>(null);

  const calculatePosition = (index: number, total: number, radius: number) => {
    const angle = (index / total) * 2 * Math.PI;
    const x = radius * Math.cos(angle);
    const y = radius * Math.sin(angle);
    return { x, y };
  };

  // Simulate real-time transactions
  useEffect(() => {
    const interval = setInterval(() => {
      const businesses = partners.filter(p => p.type === 'business');
      const individuals = partners.filter(p => p.type === 'individual');
      
      if (businesses.length && individuals.length) {
        const from = individuals[Math.floor(Math.random() * individuals.length)];
        const to = businesses[Math.floor(Math.random() * businesses.length)];
        
        const newTransaction: Transaction = {
          id: Math.random().toString(),
          from: from.id,
          to: to.id,
          amount: Math.floor(Math.random() * 100000) + 10000,
          status: 'matching'
        };

        setActiveTransactions(prev => [...prev, newTransaction]);

        // Remove transaction after animation
        setTimeout(() => {
          setActiveTransactions(prev => prev.filter(t => t.id !== newTransaction.id));
        }, 2000);
      }
    }, 3000);

    return () => clearInterval(interval);
  }, [partners]);

  return (
    <div className="relative w-[800px] h-[800px] mx-auto bg-gradient-to-br from-slate-900 to-slate-800 rounded-full p-8" ref={containerRef}>
      {/* Animated background effects */}
      <div className="absolute inset-0 rounded-full overflow-hidden">
        <div className="absolute inset-0 bg-grid-white/5 [mask-image:radial-gradient(ellipse_at_center,transparent_20%,black)]" />
        <motion.div
          className="absolute inset-0 bg-gradient-to-r from-primary/20 to-secondary/20"
          animate={{
            rotate: [0, 360],
          }}
          transition={{
            duration: 20,
            repeat: Infinity,
            ease: "linear"
          }}
        />
      </div>

      {/* Center circle representing LendingVerse */}
      <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2">
        <motion.div
          className="w-40 h-40 bg-gradient-to-br from-primary to-primary/80 rounded-full flex items-center justify-center shadow-lg backdrop-blur-xl"
          initial={{ scale: 0 }}
          animate={{ scale: 1 }}
          transition={{ duration: 0.5 }}
        >
          <motion.span 
            className="text-primary-foreground font-bold text-2xl"
            animate={{
              opacity: [1, 0.8, 1],
            }}
            transition={{
              duration: 2,
              repeat: Infinity,
              ease: "easeInOut"
            }}
          >
            LendingVerse
          </motion.span>
        </motion.div>
      </div>

      {/* Active transactions */}
      <AnimatePresence>
        {activeTransactions.map(transaction => {
          const fromPartner = partners.find(p => p.id === transaction.from);
          const toPartner = partners.find(p => p.id === transaction.to);
          if (!fromPartner || !toPartner) return null;

          const fromIndex = partners.indexOf(fromPartner);
          const toIndex = partners.indexOf(toPartner);
          const fromPos = calculatePosition(fromIndex, partners.length, 300);
          const toPos = calculatePosition(toIndex, partners.length, 300);

          return (
            <TransactionAnimation
              key={transaction.id}
              fromPosition={fromPos}
              toPosition={toPos}
              transaction={transaction}
            />
          );
        })}
      </AnimatePresence>

      {/* Partner nodes */}
      {partners.map((partner, index) => {
        const { x, y } = calculatePosition(index, partners.length, 300);
        const isRequesting = partner.status === 'requesting';
        
        return (
          <motion.div
            key={partner.id}
            className="absolute"
            style={{
              left: '50%',
              top: '50%',
            }}
            initial={{ scale: 0, x: 0, y: 0 }}
            animate={{
              scale: 1,
              x: x,
              y: y,
            }}
            transition={{ duration: 0.5, delay: index * 0.1 }}
            onHoverStart={() => setHoveredPartner(partner)}
            onHoverEnd={() => setHoveredPartner(null)}
          >
            <div className="relative -translate-x-1/2 -translate-y-1/2">
              <motion.div
                className={`w-24 h-24 rounded-full flex items-center justify-center shadow-lg backdrop-blur-sm
                  ${partner.type === 'business' 
                    ? 'bg-blue-500/20 border-blue-400/50' 
                    : 'bg-green-500/20 border-green-400/50'} 
                  border-2`}
                whileHover={{ scale: 1.1 }}
                animate={isRequesting ? {
                  boxShadow: [
                    '0 0 0 0 rgba(220, 38, 38, 0.4)',
                    '0 0 0 20px rgba(220, 38, 38, 0)'
                  ]
                } : {}}
                transition={isRequesting ? {
                  duration: 1.5,
                  repeat: Infinity,
                } : {}}
              >
                <img
                  src={partner.logo}
                  alt={partner.name}
                  className="w-16 h-16 object-contain"
                />
              </motion.div>
              
              {/* Partner name with fade effect */}
              <motion.div
                className="absolute top-full mt-2 left-1/2 -translate-x-1/2 text-center"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.2 }}
              >
                <span className="whitespace-nowrap text-sm font-medium text-white/80">
                  {partner.name}
                </span>
                {isRequesting && (
                  <div className="text-xs text-red-400 mt-1">
                    Requesting: ${partner.requestAmount?.toLocaleString()}
                  </div>
                )}
              </motion.div>
            </div>
          </motion.div>
        );
      })}

      {/* Connection lines */}
      <svg
        className="absolute inset-0 w-full h-full pointer-events-none"
        style={{ zIndex: -1 }}
      >
        {partners.map((partner, index) => {
          const { x, y } = calculatePosition(index, partners.length, 300);
          return (
            <motion.line
              key={partner.id}
              x1="50%"
              y1="50%"
              x2={`calc(50% + ${x}px)`}
              y2={`calc(50% + ${y}px)`}
              stroke="rgba(255,255,255,0.1)"
              strokeWidth="2"
              initial={{ pathLength: 0 }}
              animate={{ pathLength: 1 }}
              transition={{ duration: 1, delay: index * 0.1 }}
            />
          );
        })}
      </svg>
    </div>
  );
}