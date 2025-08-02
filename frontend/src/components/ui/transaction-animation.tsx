'use client';

import { motion, AnimatePresence } from 'framer-motion';
import { useEffect, useState } from 'react';

interface Transaction {
  id: string;
  from: string;
  to: string;
  amount: number;
  status: 'pending' | 'matching' | 'completed';
}

interface TransactionAnimationProps {
  fromPosition: { x: number; y: number };
  toPosition: { x: number; y: number };
  transaction: Transaction;
}

export function TransactionAnimation({ fromPosition, toPosition, transaction }: TransactionAnimationProps) {
  return (
    <motion.div
      className="absolute w-6 h-6 rounded-full bg-primary/30 backdrop-blur-sm"
      initial={{ 
        x: fromPosition.x, 
        y: fromPosition.y,
        scale: 0 
      }}
      animate={{ 
        x: toPosition.x, 
        y: toPosition.y,
        scale: [0, 1.2, 1],
      }}
      exit={{ scale: 0, opacity: 0 }}
      transition={{ 
        duration: 2,
        ease: "easeInOut"
      }}
    >
      <motion.div
        className="absolute inset-0 rounded-full bg-primary"
        animate={{
          scale: [1, 1.2, 1],
        }}
        transition={{
          duration: 1,
          repeat: Infinity,
        }}
      />
    </motion.div>
  );
}